#!/usr/bin/env python3
"""
Test script for the automatic trading agent
"""

import asyncio
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

async def test_trading_agent():
    """Test the trading agent functionality"""
    print("🚀 Testing Trading Agent Automatic Buy/Sell Logic")
    
    try:
        # Import the agent functions
        from src.agent import calculate_trade_decision, get_trading_client
        from src.agent_log_stream import manager
        
        # Test different scenarios
        scenarios = [
            {
                "name": "Strong Buy Signal",
                "current_price": 100.0,
                "predicted_price": 105.0,  # 5% increase
                "position_qty": 0,
                "expected_action": "BUY"
            },
            {
                "name": "Strong Sell Signal", 
                "current_price": 100.0,
                "predicted_price": 95.0,  # 5% decrease
                "position_qty": 10,
                "expected_action": "SELL"
            },
            {
                "name": "Hold Signal - Small Change",
                "current_price": 100.0,
                "predicted_price": 100.5,  # 0.5% increase (below threshold)
                "position_qty": 0,
                "expected_action": "HOLD"
            },
            {
                "name": "Add to Position",
                "current_price": 100.0,
                "predicted_price": 110.0,  # 10% increase (strong signal)
                "position_qty": 10,
                "expected_action": "BUY"
            }
        ]
        
        print("\n📊 Testing Trading Decision Logic:")
        print("-" * 60)
        
        for scenario in scenarios:
            print(f"\n🔍 Scenario: {scenario['name']}")
            print(f"   Current Price: ${scenario['current_price']:.2f}")
            print(f"   Predicted Price: ${scenario['predicted_price']:.2f}")
            print(f"   Current Position: {scenario['position_qty']} shares")
            
            decision = await calculate_trade_decision(
                current_price=scenario['current_price'],
                predicted_price=scenario['predicted_price'],
                position_qty=scenario['position_qty'],
                confidence_threshold=0.02  # 2% threshold
            )
            
            print(f"   💡 Decision: {decision['action']} {decision['qty']} shares")
            print(f"   📝 Reason: {decision['reason']}")
            
            if decision['action'] == scenario['expected_action']:
                print("   ✅ PASS - Decision matches expected")
            else:
                print(f"   ❌ FAIL - Expected {scenario['expected_action']}, got {decision['action']}")
        
        print("\n" + "=" * 60)
        print("🎯 Trading Logic Test Complete!")
        
        # Test Alpaca connection
        print("\n🔗 Testing Alpaca API Connection...")
        try:
            client = get_trading_client()
            account = client.get_account()
            print(f"✅ Connected to Alpaca successfully!")
            print(f"   Account Status: {account.status}")
            print(f"   Paper Trading: {account.account_id}")
        except Exception as e:
            print(f"❌ Alpaca connection failed: {e}")
        
        print("\n🚀 All tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_trading_agent())
