import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY', '')
DEFILLAMA_API_KEY = os.getenv('DEFILLAMA_API_KEY', '')
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY', '')

# Stablecoin Configuration
STABLECOINS = {
    'USDT': {
        'symbol': 'USDT',
        'name': 'Tether',
        'address': '0xdAC17F958D2ee523a2206206994597C13D831ec7',  # Ethereum USDT
        'target_price': 1.0,
        'decimals': 6
    },
    'USDC': {
        'symbol': 'USDC',
        'name': 'USD Coin',
        'address': '0xA0b86a33E6441b8c4C8C8C8C8C8C8C8C8C8C8C8',  # Ethereum USDC
        'target_price': 1.0,
        'decimals': 6
    },
    'DAI': {
        'symbol': 'DAI',
        'name': 'Dai',
        'address': '0x6B175474E89094C44Da98b954EedeAC495271d0F',  # Ethereum DAI
        'target_price': 1.0,
        'decimals': 18
    }
}

# API Endpoints
COINGECKO_BASE_URL = 'https://api.coingecko.com/api/v3'
DEFILLAMA_BASE_URL = 'https://api.llama.fi'
ETHERSCAN_BASE_URL = 'https://api.etherscan.io/api'

# Dashboard Configuration
REFRESH_INTERVAL = 300  # 5 minutes
ANOMALY_THRESHOLD = 0.02  # 2% deviation from peg
CHART_HISTORY_DAYS = 30
