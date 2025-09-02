#!/usr/bin/env python3
"""
Local development script for Stablecoin Tracker Dashboard
Run this script to start the dashboard locally without Docker
"""

import os
import sys
import asyncio
import threading
import time
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from data_collectors import DataAggregator
from config import STABLECOINS, ANOMALY_THRESHOLD

def setup_environment():
    """Setup environment variables for local development"""
    env_file = Path('.env')
    if env_file.exists():
        print("📝 Loading environment variables from .env file...")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    else:
        print("⚠️  No .env file found. Using default configuration.")
        print("   Create a .env file with your API keys for better performance.")

def run_data_collector():
    """Run data collector in background thread"""
    print("🔄 Starting background data collection...")
    
    async def collect_data():
        aggregator = DataAggregator()
        while True:
            try:
                print("📊 Collecting stablecoin data...")
                data = await aggregator.collect_all_data()
                if data:
                    print(f"✅ Data collected at {data.get('timestamp', 'unknown')}")
                else:
                    print("❌ Failed to collect data")
                
                # Collect historical data
                for symbol in STABLECOINS.keys():
                    hist_data = await aggregator.get_historical_data(symbol)
                    if not hist_data.empty:
                        print(f"📈 Historical data collected for {symbol}")
                
            except Exception as e:
                print(f"❌ Error in data collection: {e}")
            
            print(f"⏳ Waiting 5 minutes before next update...")
            await asyncio.sleep(300)  # 5 minutes
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(collect_data())

def main():
    """Main function to start the dashboard"""
    print("🚀 Starting Stablecoin Tracker Dashboard (Local Development)")
    print("=" * 60)
    
    # Setup environment
    setup_environment()
    
    # Check for required packages
    try:
        import dash
        import plotly
        import pandas
        print("✅ All required packages are installed")
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("   Please install requirements: pip install -r requirements.txt")
        return
    
    # Start data collector in background
    data_thread = threading.Thread(target=run_data_collector, daemon=True)
    data_thread.start()
    
    # Import and run the Dash app
    try:
        from app import app
        print("🌐 Starting web dashboard...")
        print("   Dashboard will be available at: http://localhost:8050")
        print("   Press Ctrl+C to stop")
        print("-" * 60)
        
        app.run_server(
            debug=True,
            host='0.0.0.0',
            port=8050,
            use_reloader=False  # Disable reloader to avoid conflicts
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        return

if __name__ == '__main__':
    main()
