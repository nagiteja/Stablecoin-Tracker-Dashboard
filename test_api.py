#!/usr/bin/env python3

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_collectors import DataAggregator

async def test_apis():
    print("🧪 Testing API Integration...")
    
    aggregator = DataAggregator()
    
    print("\n1. Testing CoinGecko API...")
    try:
        symbols = ['USDT', 'USDC', 'DAI']
        prices = await aggregator.coingecko.get_stablecoin_prices(symbols)
        if prices and any(prices.values()):
            print("✅ CoinGecko API working!")
            for symbol, data in prices.items():
                if data:
                    print(f"   {symbol.upper()}: ${data.get('usd', 'N/A')}")
        else:
            print("❌ CoinGecko API failed")
    except Exception as e:
        print(f"❌ CoinGecko error: {e}")
    
    print("\n2. Testing Binance API...")
    try:
        symbols = ['USDT', 'USDC', 'DAI']
        prices = await aggregator.binance.get_stablecoin_prices(symbols)
        if prices and any(prices.values()):
            print("✅ Binance API working!")
            for symbol, data in prices.items():
                if data:
                    print(f"   {symbol.upper()}: ${data.get('usd', 'N/A')}")
        else:
            print("❌ Binance API failed")
    except Exception as e:
        print(f"❌ Binance error: {e}")
    
    print("\n3. Testing Data Aggregator...")
    try:
        all_data = await aggregator.collect_all_data()
        if all_data and any(all_data.values()):
            print("✅ Data Aggregator working!")
            for symbol, data in all_data.items():
                if data:
                    print(f"   {symbol}: ${data.get('price', 'N/A')}")
        else:
            print("❌ Data Aggregator failed")
    except Exception as e:
        print(f"❌ Data Aggregator error: {e}")

if __name__ == "__main__":
    asyncio.run(test_apis())
