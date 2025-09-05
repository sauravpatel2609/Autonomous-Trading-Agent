# src/stop_loss_manager.py
"""
Stop-loss and take-profit order manager for when the agent is stopped.
This ensures your positions are protected even when the agent isn't running.
"""

import asyncio
from typing import Optional
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, StopOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.common.exceptions import APIError
from src.config import ALPACA_API_KEY, ALPACA_API_SECRET

class StopLossManager:
    """Manages protective orders when the trading agent is stopped."""
    
    def __init__(self):
        self.trading_client = TradingClient(ALPACA_API_KEY, ALPACA_API_SECRET, paper=True)
    
    async def place_stop_loss_order(self, ticker: str, stop_loss_pct: float = 0.05):
        """
        Place a stop-loss order for existing positions.
        
        Args:
            ticker: Stock symbol
            stop_loss_pct: Stop loss percentage (default 5% = 0.05)
        """
        try:
            # Get current position
            position = self.trading_client.get_open_position(ticker)
            if not position:
                print(f"❌ No position found for {ticker}")
                return
            
            # Get position details
            qty = abs(float(getattr(position, 'qty', 0)))
            side = getattr(position, 'side', 'long')
            avg_entry_price = float(getattr(position, 'avg_entry_price', 0))
            
            if qty == 0:
                print(f"❌ No shares to protect for {ticker}")
                return
            
            print(f"📊 Current Position: {qty} shares of {ticker} at ${avg_entry_price:.2f}")
            
            # Calculate stop-loss price
            if side == 'long':
                stop_loss_price = avg_entry_price * (1 - stop_loss_pct)
                order_side = OrderSide.SELL
            else:  # short position
                stop_loss_price = avg_entry_price * (1 + stop_loss_pct)
                order_side = OrderSide.BUY
            
            print(f"🛡️  Setting up stop-loss order:")
            print(f"   Stop Loss: ${stop_loss_price:.2f} ({stop_loss_pct*100:.1f}% protection)")
            
            # Place stop-loss order using StopOrderRequest
            try:
                stop_order_request = StopOrderRequest(
                    symbol=ticker,
                    qty=int(qty),
                    side=order_side,
                    time_in_force=TimeInForce.GTC,  # Good Till Cancelled
                    stop_price=stop_loss_price
                )
                stop_order = self.trading_client.submit_order(order_data=stop_order_request)
                order_id = getattr(stop_order, 'id', 'Unknown')
                print(f"✅ Stop-loss order placed: {order_id}")
                return order_id
                
            except APIError as e:
                print(f"❌ Failed to place stop-loss: {e}")
            except Exception as e:
                print(f"❌ Error placing stop-loss: {e}")
                
        except Exception as e:
            print(f"❌ Error setting up stop-loss order: {e}")
    
    async def place_take_profit_order(self, ticker: str, take_profit_pct: float = 0.10):
        """
        Place a take-profit (limit) order for existing positions.
        
        Args:
            ticker: Stock symbol
            take_profit_pct: Take profit percentage (default 10% = 0.10)
        """
        try:
            # Get current position
            position = self.trading_client.get_open_position(ticker)
            if not position:
                print(f"❌ No position found for {ticker}")
                return
            
            # Get position details
            qty = abs(float(getattr(position, 'qty', 0)))
            side = getattr(position, 'side', 'long')
            avg_entry_price = float(getattr(position, 'avg_entry_price', 0))
            
            if qty == 0:
                print(f"❌ No shares to protect for {ticker}")
                return
            
            # Calculate take-profit price
            if side == 'long':
                take_profit_price = avg_entry_price * (1 + take_profit_pct)
                order_side = OrderSide.SELL
            else:  # short position
                take_profit_price = avg_entry_price * (1 - take_profit_pct)
                order_side = OrderSide.BUY
            
            print(f"📈 Setting up take-profit order:")
            print(f"   Take Profit: ${take_profit_price:.2f} ({take_profit_pct*100:.1f}% target)")
            
            # Place take-profit order using LimitOrderRequest
            try:
                limit_order_request = LimitOrderRequest(
                    symbol=ticker,
                    qty=int(qty),
                    side=order_side,
                    time_in_force=TimeInForce.GTC,
                    limit_price=take_profit_price
                )
                
                take_profit_order = self.trading_client.submit_order(order_data=limit_order_request)
                order_id = getattr(take_profit_order, 'id', 'Unknown')
                print(f"✅ Take-profit order placed: {order_id}")
                return order_id
                
            except APIError as e:
                print(f"❌ Failed to place take-profit: {e}")
            except Exception as e:
                print(f"❌ Error placing take-profit: {e}")
                
        except Exception as e:
            print(f"❌ Error setting up take-profit order: {e}")
    
    async def emergency_sell_all(self, ticker: str):
        """
        Emergency market sell of all positions in a ticker.
        
        Args:
            ticker: Stock symbol
        """
        try:
            position = self.trading_client.get_open_position(ticker)
            if not position:
                print(f"❌ No position found for {ticker}")
                return
            
            qty = abs(float(getattr(position, 'qty', 0)))
            side = getattr(position, 'side', 'long')
            
            if qty == 0:
                print(f"❌ No shares to sell for {ticker}")
                return
            
            print(f"� EMERGENCY SELL: {qty} shares of {ticker}")
            
            # Place immediate market sell order
            market_order_request = MarketOrderRequest(
                symbol=ticker,
                qty=int(qty),
                side=OrderSide.SELL if side == 'long' else OrderSide.BUY,
                time_in_force=TimeInForce.DAY
            )
            
            sell_order = self.trading_client.submit_order(order_data=market_order_request)
            order_id = getattr(sell_order, 'id', 'Unknown')
            print(f"✅ Emergency sell order placed: {order_id}")
            return order_id
            
        except Exception as e:
            print(f"❌ Emergency sell failed: {e}")
    
    async def cancel_all_orders(self, ticker: str):
        """Cancel all pending orders for a specific ticker."""
        try:
            # Get all orders (this is a simplified approach)
            orders = self.trading_client.get_orders()
            
            ticker_orders = []
            for order in orders:
                if getattr(order, 'symbol', '') == ticker:
                    ticker_orders.append(order)
            
            if not ticker_orders:
                print(f"ℹ️  No open orders for {ticker}")
                return
            
            print(f"🗑️  Cancelling {len(ticker_orders)} open orders for {ticker}...")
            
            for order in ticker_orders:
                try:
                    order_id = getattr(order, 'id', None)
                    if order_id:
                        self.trading_client.cancel_order_by_id(order_id)
                        print(f"   ✅ Cancelled order {order_id}")
                except APIError as e:
                    print(f"   ❌ Failed to cancel order: {e}")
                except Exception as e:
                    print(f"   ❌ Error cancelling order: {e}")
                    
        except Exception as e:
            print(f"❌ Error cancelling orders: {e}")

async def main():
    """Interactive script to set up protective orders when stopping the agent."""
    
    manager = StopLossManager()
    
    print("🛡️  STOP-LOSS MANAGER")
    print("=" * 50)
    print("This tool helps protect your positions when the agent is stopped.")
    print()
    
    ticker = input("📊 Enter stock ticker (e.g., AAPL): ").upper().strip()
    if not ticker:
        print("❌ No ticker provided. Exiting.")
        return
    
    print("\n🔧 Choose protection strategy:")
    print("1. Place stop-loss order (protects against losses)")
    print("2. Place take-profit order (locks in gains)")
    print("3. Place both stop-loss AND take-profit")
    print("4. Emergency sell ALL shares immediately")
    print("5. Cancel all existing orders")
    print("6. Exit")
    
    choice = input("\n👉 Enter choice (1-6): ").strip()
    
    if choice == "1":
        print("\n⚙️  Setting up stop-loss order...")
        stop_loss = float(input("Stop-loss percentage (e.g., 0.05 for 5%): ") or "0.05")
        await manager.place_stop_loss_order(ticker, stop_loss)
        
    elif choice == "2":
        print("\n⚙️  Setting up take-profit order...")
        take_profit = float(input("Take-profit percentage (e.g., 0.10 for 10%): ") or "0.10")
        await manager.place_take_profit_order(ticker, take_profit)
        
    elif choice == "3":
        print("\n⚙️  Setting up stop-loss and take-profit orders...")
        stop_loss = float(input("Stop-loss percentage (e.g., 0.05 for 5%): ") or "0.05")
        take_profit = float(input("Take-profit percentage (e.g., 0.10 for 10%): ") or "0.10")
        await manager.place_stop_loss_order(ticker, stop_loss)
        await manager.place_take_profit_order(ticker, take_profit)
        
    elif choice == "4":
        confirm = input(f"⚠️  Are you sure you want to sell ALL {ticker} shares immediately? (yes/no): ")
        if confirm.lower() == 'yes':
            await manager.emergency_sell_all(ticker)
        else:
            print("❌ Emergency sell cancelled.")
        
    elif choice == "5":
        print(f"\n⚙️  Cancelling all orders for {ticker}...")
        await manager.cancel_all_orders(ticker)
        
    elif choice == "6":
        print("👋 Goodbye!")
        return
        
    else:
        print("❌ Invalid choice.")
        
    print(f"\n✅ Protection setup complete for {ticker}!")
    print("💡 These orders will execute automatically even when the agent is stopped.")

if __name__ == "__main__":
    asyncio.run(main())
