# src/api.py

import numpy as np
import asyncio
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import DataFeed
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from bson import json_util
import json
from fastapi import WebSocket

from src.agent_log_stream import manager
from src.config import ALPACA_API_KEY, ALPACA_API_SECRET
from src.preprocessing import create_features
from src.globals import ml_models
import src.globals as globals_module
from src.db import db
from src.schemas import UserCreate, Token
from src.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
)
from fastapi.security import OAuth2PasswordRequestForm
from src.agent import run_agent_loop

router = APIRouter()

# --- PUBLIC ENDPOINTS ---

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.get("/current_price/{ticker}")
async def get_current_price(ticker: str):
    """Get current stock price from Alpaca."""
    try:
        data_client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_API_SECRET)
        end_time = datetime.now() - timedelta(minutes=1)
        start_time = end_time - timedelta(days=1)
        
        request_params = StockBarsRequest(
            symbol_or_symbols=ticker.upper(),
            timeframe=TimeFrame.Minute,
            start=start_time,
            end=end_time,
            feed=DataFeed.IEX
        )
        bars = data_client.get_stock_bars(request_params)
        
        # Handle the bars response properly
        if hasattr(bars, 'df'):
            data = bars.df.reset_index()
        else:
            # Convert to DataFrame if it's not already
            data = bars.data[ticker.upper()]
            import pandas as pd
            data = pd.DataFrame([{
                'timestamp': bar.timestamp,
                'close': bar.close,
            } for bar in data])
        
        if len(data) == 0:
            raise HTTPException(status_code=404, detail=f"No recent price data for {ticker}")
            
        current_price = float(data['close'].iloc[-1])
        
        return {
            "ticker": ticker.upper(),
            "current_price": current_price,
            "timestamp": data['timestamp'].iloc[-1].isoformat() if hasattr(data['timestamp'].iloc[-1], 'isoformat') else str(data['timestamp'].iloc[-1])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching current price: {str(e)}")

@router.get("/predict/{ticker}")
async def predict_stock(ticker: str):
    """
    Predicts the next closing price using the Alpaca API for data.
    """
    try:
        data_client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_API_SECRET)
        end_time = datetime.now() - timedelta(minutes=15)
        start_time = end_time - timedelta(days=120)
        
        request_params = StockBarsRequest(
            symbol_or_symbols=ticker.upper(),
            timeframe=TimeFrame.Day,
            start=start_time,
            end=end_time,
            feed=DataFeed.IEX # Use the free IEX data feed
        )
        bars = data_client.get_stock_bars(request_params)
        data = bars.df.rename(columns={'close': 'Close', 'open': 'Open', 'high': 'High', 'low': 'Low', 'volume': 'Volume'})
        
        if len(data) < 60:
            raise HTTPException(status_code=400, detail="Not enough historical data for prediction.")

        featured_data = create_features(data)
        features_for_prediction = [col for col in featured_data.columns if 'feature_' in col]
        
        model = ml_models.get('lstm')
        scaler_features = ml_models.get('scaler_features')
        scaler_target = ml_models.get('scaler_target')

        last_60_days = featured_data[features_for_prediction].tail(60)
        scaled_features = scaler_features.transform(last_60_days)
        input_data = np.reshape(scaled_features, (1, 60, len(features_for_prediction)))
        
        predicted_scaled = model.predict(input_data)
        predicted_price = scaler_target.inverse_transform(predicted_scaled)[0][0]

        return {
            "ticker": ticker,
            "last_close": data['Close'].iloc[-1],
            "predicted_next_close": float(predicted_price)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stock-data/{symbol}")
async def get_stock_data(symbol: str):
    """
    Fetches historical stock data from Alpaca for charting.
    """
    try:
        data_client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_API_SECRET)
        end_time = datetime.now() - timedelta(minutes=15)
        start_time = end_time - timedelta(days=90)
        
        request_params = StockBarsRequest(
            symbol_or_symbols=symbol.upper(),
            timeframe=TimeFrame.Day,
            start=start_time,
            end=end_time,
            feed=DataFeed.IEX
        )
        bars = data_client.get_stock_bars(request_params)
        data = bars.df.reset_index()
        
        if data.empty:
            raise HTTPException(status_code=404, detail=f"No data for {symbol}")
            
        data['timestamp'] = data['timestamp'].apply(lambda x: x.isoformat())
        return data[['timestamp', 'close']].rename(columns={'timestamp': 'Date', 'close': 'Close'}).to_dict('records')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- AUTHENTICATION ENDPOINTS ---

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    if db.users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db.users.insert_one({"username": user.username, "hashed_password": hashed_password})
    return {"message": "User created successfully"}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.users.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# --- PROTECTED, USER-SPECIFIC ENDPOINTS ---

@router.get("/account")
async def get_account(current_user: dict = Depends(get_current_user)):
    """Get Alpaca account information including cash balance and portfolio value."""
    try:
        trading_client = TradingClient(ALPACA_API_KEY, ALPACA_API_SECRET, paper=True)
        account = trading_client.get_account()
        return {
            "cash": float(account.cash),
            "portfolio_value": float(account.portfolio_value),
            "buying_power": float(account.buying_power),
            "equity": float(account.equity)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/portfolio")
async def get_portfolio(current_user: dict = Depends(get_current_user)):
    try:
        trading_client = TradingClient(ALPACA_API_KEY, ALPACA_API_SECRET, paper=True)
        positions = trading_client.get_all_positions()
        portfolio_data = [
            {"symbol": pos.symbol, "quantity": float(pos.qty), "market_value": float(pos.market_value)}
            for pos in positions
        ]
        return portfolio_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trades", response_model=List[dict])
async def get_trades(current_user: dict = Depends(get_current_user)):
    try:
        trades = db.trades.find({"username": current_user["username"]}).sort("timestamp", -1).limit(20)
        trades_list = json.loads(json_util.dumps(list(trades)))
        return trades_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- REAL-TIME LOG STREAMING ---

@router.websocket("/ws/agent-logs")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text() # Keep connection alive
    except Exception:
        manager.disconnect(websocket)

# --- AGENT CONTROL ENDPOINTS ---

@router.post("/agent/start")
async def start_agent(request: dict, current_user: dict = Depends(get_current_user)):
    """Start the trading agent for a specific ticker with automatic buy/sell logic."""
    
    ticker = request.get("stock", "AAPL").upper()
    
    if globals_module.agent_running:
        return {"status": "error", "message": f"Agent is already running for {globals_module.current_ticker}"}
    
    try:
        # Start the enhanced agent with auto-trading
        globals_module.agent_task = asyncio.create_task(run_agent_loop(ticker))
        globals_module.agent_running = True
        globals_module.current_ticker = ticker
        
        await manager.broadcast(f"🚀 AUTO-TRADING AGENT STARTED for {ticker} by {current_user['username']}")
        await manager.broadcast(f"📈 Agent will automatically BUY and SELL based on AI predictions")
        await manager.broadcast(f"🛡️ Protective orders will be placed automatically when stopped")
        
        return {
            "status": "success", 
            "message": f"Auto-trading agent started for {ticker}. Will buy/sell automatically based on predictions.",
            "ticker": ticker
        }
    except Exception as e:
        await manager.broadcast(f"❌ Failed to start agent: {str(e)}")
        return {"status": "error", "message": f"Failed to start agent: {str(e)}"}

@router.post("/agent/stop")
async def stop_agent(current_user: dict = Depends(get_current_user)):
    """Stop the trading agent and automatically place protective orders."""
    
    if not globals_module.agent_running:
        return {"status": "error", "message": "No agent is currently running"}
    
    try:
        stopped_ticker = globals_module.current_ticker
        
        if globals_module.agent_task:
            globals_module.agent_task.cancel()
            try:
                await globals_module.agent_task
            except asyncio.CancelledError:
                pass
        
        await manager.broadcast(f"🛑 AGENT STOPPED by user {current_user['username']}")
        await manager.broadcast(f"🛡️ Automatic protective orders were set up during shutdown")
        await manager.broadcast(f"💡 Your positions are now protected even when agent is offline!")
        
        globals_module.agent_running = False
        globals_module.agent_task = None
        globals_module.current_ticker = None
        
        return {
            "status": "success", 
            "message": f"Agent stopped and protective orders placed for {stopped_ticker}",
            "ticker": stopped_ticker
        }
    except Exception as e:
        await manager.broadcast(f"❌ Failed to stop agent gracefully: {str(e)}")
        # Force stop anyway
        globals_module.agent_running = False
        globals_module.agent_task = None
        globals_module.current_ticker = None
        return {"status": "error", "message": f"Agent force-stopped: {str(e)}"}

@router.get("/agent/status")
async def get_agent_status():
    """Get the current status of the trading agent."""
    return {
        "running": globals_module.agent_running,
        "ticker": globals_module.current_ticker,
        "task_id": id(globals_module.agent_task) if globals_module.agent_task else None
    }

@router.post("/agent/protect")
async def setup_protective_orders(request: dict, current_user: dict = Depends(get_current_user)):
    """Set up protective orders (stop-loss/take-profit) for a specific ticker."""
    
    ticker = request.get("ticker", "AAPL").upper()
    stop_loss_pct = request.get("stop_loss_pct", 0.05)  # 5% default
    take_profit_pct = request.get("take_profit_pct", 0.10)  # 10% default
    
    try:
        from src.stop_loss_manager import StopLossManager
        manager_instance = StopLossManager()
        
        await manager.broadcast(f"🛡️ Setting up protective orders for {ticker}...")
        
        # Place stop-loss order
        stop_order_id = await manager_instance.place_stop_loss_order(ticker, stop_loss_pct)
        
        # Place take-profit order  
        profit_order_id = await manager_instance.place_take_profit_order(ticker, take_profit_pct)
        
        await manager.broadcast(f"✅ Protective orders placed for {ticker}")
        
        return {
            "status": "success",
            "message": f"Protective orders placed for {ticker}",
            "stop_loss_order": stop_order_id,
            "take_profit_order": profit_order_id,
            "stop_loss_pct": stop_loss_pct * 100,
            "take_profit_pct": take_profit_pct * 100
        }
        
    except Exception as e:
        await manager.broadcast(f"❌ Failed to set protective orders: {str(e)}")
        return {"status": "error", "message": f"Failed to set protective orders: {str(e)}"}

@router.post("/agent/emergency-sell")
async def emergency_sell_position(request: dict, current_user: dict = Depends(get_current_user)):
    """Emergency sell all shares of a specific ticker immediately."""
    
    ticker = request.get("ticker", "AAPL").upper()
    
    try:
        from src.stop_loss_manager import StopLossManager
        manager_instance = StopLossManager()
        
        await manager.broadcast(f"🚨 EMERGENCY SELL initiated for {ticker} by {current_user['username']}")
        
        order_id = await manager_instance.emergency_sell_all(ticker)
        
        await manager.broadcast(f"✅ Emergency sell order placed for {ticker}")
        
        return {
            "status": "success",
            "message": f"Emergency sell order placed for {ticker}",
            "order_id": order_id,
            "ticker": ticker
        }
        
    except Exception as e:
        await manager.broadcast(f"❌ Emergency sell failed: {str(e)}")
        return {"status": "error", "message": f"Emergency sell failed: {str(e)}"}