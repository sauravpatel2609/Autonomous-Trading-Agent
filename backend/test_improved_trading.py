#!/usr/bin/env python3
"""
Test script for improved trading logic with better sell behavior
"""

import asyncio
import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agent import calculate_trade_decision

async def test_improved_trading_logic():
    """Test the improved trading logic with more aggressive selling."""
    
    print("🚀 Testing IMPROVED Trading Agent Logic (Better Sell Behavior)")
    print("=" * 70)
    
    # Test scenarios
    test_cases = [
        {
            "name": "Strong Buy Signal (No Position)",
            "current_price": 100.0,
            "predicted_price": 105.0,
            "position": 0,
            "expected": "BUY 10 shares"
        },
        {
            "name": "Small Downward Prediction (With Position) - Should SELL",
            "current_price": 100.0,
            "predicted_price": 99.2,  # Only 0.8% down but should still sell
            "position": 10,
            "expected": "SELL 10 shares"
        },
        {
            "name": "Any Downward Movement (With Position) - Should SELL",
            "current_price": 100.0,
            "predicted_price": 99.9,  # Even tiny 0.1% down should trigger sell
            "position": 15,
            "expected": "SELL 15 shares"
        },
        {
            "name": "Strong Downward Prediction (With Position)",
            "current_price": 100.0,
            "predicted_price": 95.0,
            "position": 20,
            "expected": "SELL 20 shares"
        },
        {
            "name": "Strong Upward (Add to Position)",
            "current_price": 100.0,
            "predicted_price": 110.0,
            "position": 10,
            "expected": "BUY 5 shares"
        },
        {
            "name": "Hold Signal - Small Upward, No Position",
            "current_price": 100.0,
            "predicted_price": 100.5,
            "position": 0,
            "expected": "HOLD"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🔍 Scenario {i}: {test['name']}")
        print(f"   Current Price: ${test['current_price']:.2f}")
        print(f"   Predicted Price: ${test['predicted_price']:.2f}")
        print(f"   Current Position: {test['position']} shares")
        
        # Calculate decision
        decision = await calculate_trade_decision(
            current_price=test['current_price'],
            predicted_price=test['predicted_price'],
            position_qty=test['position'],
            confidence_threshold=0.015  # 1.5% threshold
        )
        
        action = decision['action']
        qty = decision['qty']
        reason = decision['reason']
        
        print(f"   💡 Decision: {action} {qty} shares")
        print(f"   📝 Reason: {reason}")
        
        # Check if it matches expected behavior
        if action == "HOLD":
            result_str = "HOLD"
        else:
            result_str = f"{action} {qty} shares"
            
        if test['expected'] in result_str:
            print(f"   ✅ PASS - Decision matches expected")
        else:
            print(f"   ❌ FAIL - Expected: {test['expected']}, Got: {result_str}")
    
    print("\n" + "=" * 70)
    print("🎯 Improved Trading Logic Test Complete!")
    print("\n📈 Key Improvements:")
    print("   • More aggressive selling on ANY downward prediction")
    print("   • Lower threshold for sell triggers (0.75% instead of 1.5%)")  
    print("   • Better position protection")
    print("   • Enhanced logging for debugging")

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_improved_trading_logic())
