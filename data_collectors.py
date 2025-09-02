import asyncio
import aiohttp
import requests
import pandas as pd
from datetime import datetime, timedelta
import time
from typing import Dict, List, Optional
import logging
from asyncio_throttle import Throttler

from config import (
    COINGECKO_BASE_URL, DEFILLAMA_BASE_URL, ETHERSCAN_BASE_URL,
    STABLECOINS, COINGECKO_API_KEY, ETHERSCAN_API_KEY
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CoinGeckoCollector:
    """Collects stablecoin price and market data from CoinGecko API"""
    
    def __init__(self):
        self.base_url = COINGECKO_BASE_URL
        self.api_key = COINGECKO_API_KEY
        self.throttler = Throttler(rate_limit=50, period=60)  # 50 calls per minute
        
    async def get_stablecoin_prices(self, symbols: List[str]) -> Dict:
        """Fetch current prices for stablecoins"""
        try:
            async with self.throttler:
                async with aiohttp.ClientSession() as session:
                    # Get price data for all stablecoins
                    ids = ','.join([f"{symbol.lower()}" for symbol in symbols])
                    url = f"{self.base_url}/simple/price"
                    params = {
                        'ids': ids,
                        'vs_currencies': 'usd',
                        'include_24hr_change': 'true',
                        'include_market_cap': 'true'
                    }
                    
                    if self.api_key:
                        params['x_cg_demo_api_key'] = self.api_key
                    
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            return data
                        else:
                            logger.error(f"CoinGecko API error: {response.status}")
                            return {}
        except Exception as e:
            logger.error(f"Error fetching CoinGecko data: {e}")
            return {}
    
    async def get_historical_prices(self, symbol: str, days: int = 30) -> pd.DataFrame:
        """Fetch historical price data for a stablecoin"""
        try:
            async with self.throttler:
                async with aiohttp.ClientSession() as session:
                    url = f"{self.base_url}/coins/{symbol.lower()}/market_chart"
                    params = {
                        'vs_currency': 'usd',
                        'days': days
                    }
                    
                    if self.api_key:
                        params['x_cg_demo_api_key'] = self.api_key
                    
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            # Convert to DataFrame
                            prices = data.get('prices', [])
                            df = pd.DataFrame(prices, columns=['timestamp', 'price'])
                            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                            df['date'] = df['timestamp'].dt.date
                            df['symbol'] = symbol.upper()
                            
                            return df
                        else:
                            logger.error(f"CoinGecko historical API error: {response.status}")
                            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            return pd.DataFrame()

class DeFiLlamaCollector:
    """Collects DeFi protocol data and TVL information"""
    
    def __init__(self):
        self.base_url = DEFILLAMA_BASE_URL
        
    async def get_protocol_tvl(self, protocol: str) -> Dict:
        """Fetch TVL data for a specific protocol"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/protocol/{protocol}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        logger.error(f"DeFiLlama API error: {response.status}")
                        return {}
        except Exception as e:
            logger.error(f"Error fetching DeFiLlama data: {e}")
            return {}
    
    async def get_stablecoin_tvl(self) -> Dict:
        """Fetch stablecoin TVL data"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/v2/historicalChainTvls/Ethereum"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        logger.error(f"DeFiLlama TVL API error: {response.status}")
                        return {}
        except Exception as e:
            logger.error(f"Error fetching TVL data: {e}")
            return {}

class EtherscanCollector:
    """Collects on-chain data from Etherscan API"""
    
    def __init__(self):
        self.base_url = ETHERSCAN_BASE_URL
        self.api_key = ETHERSCAN_API_KEY
        
    def get_token_supply(self, contract_address: str) -> Optional[int]:
        """Get current token supply from Etherscan"""
        try:
            url = f"{self.base_url}"
            params = {
                'module': 'stats',
                'action': 'tokensupply',
                'contractaddress': contract_address,
                'apikey': self.api_key
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == '1':
                    return int(data['result'])
                else:
                    logger.error(f"Etherscan API error: {data['message']}")
                    return None
            else:
                logger.error(f"Etherscan HTTP error: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching token supply: {e}")
            return None
    
    def get_token_holders(self, contract_address: str) -> Optional[int]:
        """Get number of token holders"""
        try:
            url = f"{self.base_url}"
            params = {
                'module': 'token',
                'action': 'tokenholderlist',
                'contractaddress': contract_address,
                'apikey': self.api_key
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == '1':
                    return len(data['result'])
                else:
                    logger.error(f"Etherscan API error: {data['message']}")
                    return None
            else:
                logger.error(f"Etherscan HTTP error: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching token holders: {e}")
            return None

class DataAggregator:
    """Aggregates data from multiple sources"""
    
    def __init__(self):
        self.coingecko = CoinGeckoCollector()
        self.defillama = DeFiLlamaCollector()
        self.etherscan = EtherscanCollector()
        
    async def collect_all_data(self) -> Dict:
        """Collect comprehensive data for all stablecoins"""
        try:
            # Collect price data
            symbols = list(STABLECOINS.keys())
            prices = await self.coingecko.get_stablecoin_prices(symbols)
            
            # Collect on-chain data
            on_chain_data = {}
            for symbol, config in STABLECOINS.items():
                supply = self.etherscan.get_token_supply(config['address'])
                holders = self.etherscan.get_token_holders(config['address'])
                
                on_chain_data[symbol] = {
                    'supply': supply,
                    'holders': holders,
                    'address': config['address']
                }
            
            # Aggregate all data
            aggregated_data = {
                'timestamp': datetime.now().isoformat(),
                'prices': prices,
                'on_chain': on_chain_data,
                'stablecoins': STABLECOINS
            }
            
            return aggregated_data
        except Exception as e:
            logger.error(f"Error aggregating data: {e}")
            return {}
    
    async def get_historical_data(self, symbol: str, days: int = 30) -> pd.DataFrame:
        """Get historical data for a specific stablecoin"""
        return await self.coingecko.get_historical_prices(symbol, days)
    
    def calculate_peg_deviation(self, current_price: float, target_price: float = 1.0) -> float:
        """Calculate deviation from peg"""
        return abs(current_price - target_price) / target_price
    
    def detect_anomalies(self, prices: List[float], threshold: float = 0.02) -> List[bool]:
        """Detect price anomalies based on threshold"""
        target_price = 1.0
        anomalies = []
        
        for price in prices:
            deviation = self.calculate_peg_deviation(price, target_price)
            anomalies.append(deviation > threshold)
        
        return anomalies
