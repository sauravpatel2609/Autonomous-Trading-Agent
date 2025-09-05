# src/agent.py
import asyncio
import httpx  # <-- Import httpx instead of requests
import argparse
import signal
import sys
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, StopOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.common.exceptions import APIError
from src.agent_log_stream import manager
from src.config import ALPACA_API_KEY, ALPACA_API_SECRET

# Global variables for graceful shutdown
shutdown_requested = False
current_ticker = None
trading_client = None

def get_trading_client():
    """Initializes and returns the Alpaca trading client."""
    return TradingClient(ALPACA_API_KEY, ALPACA_API_SECRET, paper=True)

async def setup_protective_orders_on_shutdown(ticker: str, stop_loss_pct: float = 0.03):
    """
    Automatically place stop-loss orders when the agent is being shut down.
    
    Args:
        ticker: Stock symbol
        stop_loss_pct: Stop loss percentage (default 3% = 0.03)
    """
    try:
        await manager.broadcast("🛡️ SHUTDOWN: Setting up protective orders...")
        
        client = get_trading_client()
        position = client.get_open_position(ticker)
        
        if not position:
            await manager.broadcast(f"ℹ️ No position to protect for {ticker}")
            return
        
        qty = abs(float(getattr(position, 'qty', 0)))
        side = getattr(position, 'side', 'long')
        avg_entry_price = float(getattr(position, 'avg_entry_price', 0))
        
        if qty == 0:
            await manager.broadcast(f"ℹ️ No shares to protect for {ticker}")
            return
        
        # Calculate stop-loss price (more aggressive 3% stop-loss)
        stop_loss_price = avg_entry_price * (1 - stop_loss_pct)
        
        await manager.broadcast(f"📊 Position: {qty} shares of {ticker} at ${avg_entry_price:.2f}")
        await manager.broadcast(f"🛡️ Setting stop-loss at ${stop_loss_price:.2f} ({stop_loss_pct*100:.1f}% protection)")
        
        # Place stop-loss order
        stop_order_request = StopOrderRequest(
            symbol=ticker,
            qty=int(qty),
            side=OrderSide.SELL,
            time_in_force=TimeInForce.GTC,
            stop_price=stop_loss_price
        )
        
        stop_order = client.submit_order(order_data=stop_order_request)
        order_id = getattr(stop_order, 'id', 'Unknown')
        await manager.broadcast(f"✅ PROTECTION: Stop-loss order {order_id} placed!")
        await manager.broadcast(f"💡 Your position is now protected even when agent is stopped!")
        
    except Exception as e:
        await manager.broadcast(f"❌ Failed to set protective orders: {e}")

def signal_handler(signum, frame):
    """Handle Ctrl+C and other shutdown signals."""
    global shutdown_requested
    shutdown_requested = True
    print("\n🛑 Shutdown signal received. Setting up protective orders...")

# Set up signal handlers
signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # Termination signal

async def place_order(client, symbol, qty, side):
    """Places a market order and broadcasts the result."""
    try:
        market_order_data = MarketOrderRequest(symbol=symbol, qty=qty, side=side, time_in_force=TimeInForce.DAY)
        order = client.submit_order(order_data=market_order_data)
        await manager.broadcast(f"SUCCESS: Placed {side.value} order for {qty} shares of {symbol}.")
        return order
    except Exception as e:
        await manager.broadcast(f"ERROR: Failed to place order: {e}")
        return None

async def get_current_price(client: httpx.AsyncClient, ticker: str):
    """Get current stock price from the prediction API (uses last close price)."""
    try:
        response = await client.get(f"http://localhost:8000/predict/{ticker}", timeout=10.0)
        response.raise_for_status()
        data = response.json()
        return data.get('last_close')  # Use the last close price from prediction data
    except Exception as e:
        await manager.broadcast(f"ERROR: Failed to get current price: {e}")
        return None

async def calculate_trade_decision(current_price, predicted_price, position_qty=0.0, confidence_threshold=0.02):
    """
    Calculate trading decision based on prediction vs current price.
    
    Args:
        current_price: Current stock price
        predicted_price: Predicted next close price
        position_qty: Current position quantity (positive for long, 0 for no position)
        confidence_threshold: Minimum percentage change to trigger trade (default 2%)
    
    Returns:
        dict: {'action': 'BUY'|'SELL'|'HOLD', 'qty': int, 'reason': str}
    """
    if current_price is None or predicted_price is None:
        return {'action': 'HOLD', 'qty': 0, 'reason': 'Missing price data'}
    
    price_change_pct = (predicted_price - current_price) / current_price
    
    await manager.broadcast(f"ANALYSIS: Current: ${current_price:.2f}, Predicted: ${predicted_price:.2f}, Change: {price_change_pct:.2%}")
    await manager.broadcast(f"POSITION: Currently holding {position_qty} shares")
    
    # If we predict price will go up significantly and we don't have a position
    if price_change_pct > confidence_threshold and position_qty == 0:
        return {
            'action': 'BUY',
            'qty': 10,  # Buy 10 shares
            'reason': f'Predicted {price_change_pct:.2%} increase, no current position'
        }
    
    # If we predict price will go down and we have a position - SELL AGGRESSIVELY
    elif price_change_pct < -confidence_threshold/2 and position_qty > 0:  # Lower threshold for selling
        return {
            'action': 'SELL',
            'qty': abs(int(position_qty)),  # Sell all shares
            'reason': f'Predicted {price_change_pct:.2%} decrease, closing position'
        }
    
    # If we predict price will go down significantly (any downward movement with position)
    elif price_change_pct < 0 and position_qty > 0:
        return {
            'action': 'SELL',
            'qty': abs(int(position_qty)),  # Sell all shares
            'reason': f'Any downward prediction {price_change_pct:.2%} detected, protecting position'
        }
    
    # If we predict continued upward movement and already have a position
    elif price_change_pct > confidence_threshold * 2 and position_qty > 0:
        return {
            'action': 'BUY',
            'qty': 5,  # Add 5 more shares
            'reason': f'Strong upward prediction {price_change_pct:.2%}, adding to position'
        }
    
    # Hold in all other cases
    else:
        return {
            'action': 'HOLD',
            'qty': 0,
            'reason': f'Change {price_change_pct:.2%} below threshold or position already optimal'
        }

async def wait_for_api(client: httpx.AsyncClient, api_url: str, retries: int = 20, delay: int = 10):
    """Waits for the prediction API to become available using httpx."""
    print(f"⏳ Waiting for API at {api_url} (max {retries} attempts)")
    await manager.broadcast("INFO: Agent started. Waiting for API server...")
    for i in range(retries):
        try:
            print(f"   Attempt {i+1}/{retries}: Checking API...")
            response = await client.get(api_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ API is available! Status: {response.status_code}")
                await manager.broadcast("INFO: Prediction API is available.")
                return True
        except httpx.RequestError as e:
            print(f"❌ API not available: {e}")
            await manager.broadcast(f"INFO: API not available. Retrying... ({i+1}/{retries})")
            await asyncio.sleep(delay)
    
    print("💥 Failed to connect to API after all attempts")
    return False

async def run_agent_loop(ticker: str, trade_qty: int = 10):
    """The main async loop for the trading agent with automatic buy/sell logic."""
    global shutdown_requested, current_ticker, trading_client
    current_ticker = ticker
    
    await manager.broadcast("INFO: Entering main trading loop with automatic trading enabled...")
    trading_client = get_trading_client()
    api_predict_url = f"http://localhost:8000/predict/{ticker}"
    
    async with httpx.AsyncClient() as client:
        while not shutdown_requested:
            try:
                await manager.broadcast(f"INFO: Checking market status for {ticker}...")
                
                clock = trading_client.get_clock()
                is_open = getattr(clock, 'is_open', True)  # Default to True if we can't determine
                if not is_open:
                    await manager.broadcast("INFO: Market is closed. Agent is waiting...")
                    # Check for shutdown more frequently when market is closed
                    for _ in range(90):  # 90 * 10 seconds = 15 minutes total
                        if shutdown_requested:
                            break
                        await asyncio.sleep(10)
                    continue

                await manager.broadcast("INFO: Market is OPEN. Proceeding with trading logic.")
                
                # Get current position
                position_qty = 0.0
                try:
                    position = trading_client.get_open_position(ticker)
                    if position:
                        # Position qty is always positive, side indicates long/short
                        qty = getattr(position, 'qty', 0)
                        position_qty = float(qty)
                        side = getattr(position, 'side', 'long')
                        if side == 'short':
                            position_qty = -position_qty
                        await manager.broadcast(f"INFO: Current position: {position_qty} shares ({side})")
                    else:
                        await manager.broadcast("INFO: No open position for this stock.")
                except APIError as e:
                    await manager.broadcast(f"INFO: No open position for this stock. ({str(e)})")
                except Exception as e:
                    await manager.broadcast(f"INFO: Error getting position: {str(e)}")

                # Get current price and prediction together
                await manager.broadcast("INFO: Getting prediction and current price from API...")
                response = await client.get(api_predict_url, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                current_price = data.get('last_close')
                predicted_price = data['predicted_next_close']
                
                if current_price is None:
                    await manager.broadcast("WARNING: Could not get current price, skipping this cycle")
                    await asyncio.sleep(60)
                    continue
                
                await manager.broadcast(f"INFO: Current price: ${current_price:.2f}")
                await manager.broadcast(f"INFO: Prediction received: ${predicted_price:.2f}")
                
                # Calculate trading decision
                decision = await calculate_trade_decision(
                    current_price=current_price,
                    predicted_price=predicted_price,
                    position_qty=position_qty,
                    confidence_threshold=0.015  # 1.5% threshold
                )
                
                await manager.broadcast(f"DECISION: {decision['action']} - {decision['reason']}")
                
                # Check for shutdown before executing trades
                if shutdown_requested:
                    await manager.broadcast("🛑 Shutdown requested during trading decision!")
                    break
                
                # Execute trade if needed
                if decision['action'] == 'BUY' and decision['qty'] > 0:
                    await manager.broadcast(f"EXECUTING: Buy {decision['qty']} shares of {ticker}")
                    order = await place_order(trading_client, ticker, decision['qty'], OrderSide.BUY)
                    if order:
                        await manager.broadcast(f"ORDER PLACED: Buy order {order.id} submitted")
                    
                elif decision['action'] == 'SELL' and decision['qty'] > 0:
                    await manager.broadcast(f"EXECUTING: Sell {decision['qty']} shares of {ticker}")
                    order = await place_order(trading_client, ticker, decision['qty'], OrderSide.SELL)
                    if order:
                        await manager.broadcast(f"ORDER PLACED: Sell order {order.id} submitted")
                
                else:
                    await manager.broadcast(f"NO ACTION: Holding current position")
                
                await manager.broadcast("INFO: Cycle complete. Sleeping for 5 minutes...")
                # Sleep with periodic shutdown checks
                for _ in range(60):  # 60 * 5 seconds = 5 minutes total
                    if shutdown_requested:
                        break
                    await asyncio.sleep(5)

            except asyncio.CancelledError:
                await manager.broadcast("INFO: Agent has been stopped.")
                break
            except Exception as e:
                await manager.broadcast(f"ERROR: An error occurred in agent loop: {e}")
                # Sleep with shutdown checks during error recovery
                for _ in range(12):  # 12 * 5 seconds = 1 minute total
                    if shutdown_requested:
                        break
                    await asyncio.sleep(5)
        
        # Shutdown sequence
        if shutdown_requested:
            await manager.broadcast("🛑 SHUTDOWN INITIATED: Setting up protective orders...")
            await setup_protective_orders_on_shutdown(ticker)
            await manager.broadcast("✅ Agent shutdown complete with protection enabled!")

async def main(ticker: str):
    print(f"🚀 Starting Trading Agent for {ticker}")
    health_check_url = "http://localhost:8000/health"
    async with httpx.AsyncClient() as client:
        print(f"🔗 Checking API availability at {health_check_url}")
        if await wait_for_api(client, health_check_url):
            print(f"✅ API is available, starting trading loop")
            await run_agent_loop(ticker=ticker)
        else:
            print("❌ CRITICAL: Exiting. Prediction API is not available.")
            await manager.broadcast("CRITICAL: Exiting. Prediction API is not available.")

if __name__ == "__main__":
    print("📊 Trading Agent Starting...")
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", type=str, default="AAPL")
    args = parser.parse_args()
    
    print(f"🎯 Target ticker: {args.ticker}")
    asyncio.run(main(ticker=args.ticker))