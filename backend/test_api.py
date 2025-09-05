#!/usr/bin/env python3

import httpx
import asyncio

async def test_api():
    print("🔗 Testing API connection...")
    async with httpx.AsyncClient() as client:
        try:
            # Test health endpoint
            response = await client.get('http://localhost:8000/health')
            print(f"✅ Health check: {response.status_code} - {response.text}")
            
            # Test prediction endpoint
            response = await client.get('http://localhost:8000/predict/AAPL')
            print(f"📈 Prediction: {response.status_code} - {response.text}")
            
        except Exception as e:
            print(f"❌ API Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_api())
