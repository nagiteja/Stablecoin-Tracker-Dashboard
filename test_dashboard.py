#!/usr/bin/env python3
"""
Test script for Stablecoin Tracker Dashboard
Run this to verify all components are working correctly
"""

import asyncio
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing package imports...")
    
    try:
        import dash
        print("✅ Dash imported successfully")
    except ImportError as e:
        print(f"❌ Dash import failed: {e}")
        return False
    
    try:
        import plotly
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import aiohttp
        print("✅ aiohttp imported successfully")
    except ImportError as e:
        print(f"❌ aiohttp import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import STABLECOINS, ANOMALY_THRESHOLD
        print(f"✅ Configuration loaded successfully")
        print(f"   Stablecoins: {list(STABLECOINS.keys())}")
        print(f"   Anomaly threshold: {ANOMALY_THRESHOLD}")
        return True
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False

async def test_data_collectors():
    """Test data collection functionality"""
    print("\n📊 Testing data collectors...")
    
    try:
        from data_collectors import DataAggregator
        
        aggregator = DataAggregator()
        print("✅ DataAggregator initialized successfully")
        
        # Test basic functionality
        deviation = aggregator.calculate_peg_deviation(1.02)
        print(f"✅ Peg deviation calculation: {deviation:.3f}")
        
        anomalies = aggregator.detect_anomalies([0.99, 1.01, 1.03], 0.02)
        print(f"✅ Anomaly detection: {anomalies}")
        
        return True
    except Exception as e:
        print(f"❌ Data collectors test failed: {e}")
        return False

def test_dash_app():
    """Test Dash app initialization"""
    print("\n🌐 Testing Dash app...")
    
    try:
        # Import app components
        from app import app
        print("✅ Dash app imported successfully")
        
        # Check if app has required components
        if hasattr(app, 'layout'):
            print("✅ App layout defined")
        else:
            print("❌ App layout missing")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Dash app test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Running Stablecoin Dashboard Tests")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Configuration", test_config),
        ("Data Collectors", test_data_collectors),
        ("Dash App", test_dash_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Dashboard is ready to run.")
        print("\nTo start the dashboard:")
        print("  - Docker: ./deploy.sh")
        print("  - Local: python run_local.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False
    
    return True

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite crashed: {e}")
        sys.exit(1)
