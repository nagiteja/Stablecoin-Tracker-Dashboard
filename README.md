# 🪙 Stablecoin Tracker Dashboard

A comprehensive real-time monitoring dashboard for tracking stablecoin prices, supply metrics, and peg stability for USDT, USDC, and DAI.

## ✨ Features

- **Real-time Price Monitoring**: Live price updates from CoinGecko API
- **Peg Stability Analysis**: Automatic detection of deviations from $1.00 peg
- **Supply Metrics**: On-chain token supply and holder data from Etherscan
- **Interactive Charts**: Plotly-powered visualizations with anomaly detection
- **Anomaly Detection**: Machine learning-based detection of unusual price movements
- **Multi-source Data**: Integration with CoinGecko, DeFiLlama, and Etherscan APIs
- **Responsive Design**: Modern Bootstrap-based UI that works on all devices

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Dashboard │    │  Data Collectors│    │   External APIs │
│   (Dash/Plotly) │◄──►│  (Async/Thread)│◄──►│  (CoinGecko,    │
│                 │    │                 │    │   Etherscan)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│  Data Storage  │◄─────────────┘
                        │  (In-memory)   │
                        └─────────────────┘
```

## 🚀 Quick Start

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Stablecoin-Tracker-Dashboard
   ```

2. **Make deployment script executable**
   ```bash
   chmod +x deploy.sh
   ```

3. **Run the deployment script**
   ```bash
   ./deploy.sh
   ```

4. **Access your dashboard**
   - Local: http://localhost:8050
   - Nginx (SSL): https://localhost

### Option 2: Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

3. **Run the dashboard**
   ```bash
   python run_local.py
   ```

4. **Access at**: http://localhost:8050

## 🔑 API Keys Setup

For optimal performance, obtain API keys from:

- **CoinGecko**: [https://www.coingecko.com/en/api](https://www.coingecko.com/en/api)
- **Etherscan**: [https://etherscan.io/apis](https://etherscan.io/apis)
- **DeFiLlama**: [https://defillama.com/docs/api](https://defillama.com/docs/api)

Add them to your `.env` file:
```bash
COINGECKO_API_KEY=your_key_here
ETHERSCAN_API_KEY=your_key_here
DEFILLAMA_API_KEY=your_key_here
```

## 📊 Dashboard Components

### 1. Status Cards
- Real-time price display for each stablecoin
- Color-coded indicators for peg stability
- 24-hour price change percentages

### 2. Interactive Charts
- Time-series price charts with anomaly detection
- Peg deviation analysis
- Historical data visualization

### 3. Supply Metrics
- Current token supply from blockchain
- Number of token holders
- Market capitalization data

### 4. Stability Analysis
- Real-time peg deviation calculations
- Anomaly detection alerts
- Stability status indicators

### 5. Detailed Metrics Table
- Comprehensive data view
- Sortable columns
- Export capabilities

## 🛠️ Configuration

Key configuration options in `config.py`:

```python
# Refresh intervals
REFRESH_INTERVAL = 300  # 5 minutes

# Anomaly detection
ANOMALY_THRESHOLD = 0.02  # 2% deviation

# Chart history
CHART_HISTORY_DAYS = 30
```

## 🔧 Management Commands

### Docker Commands
```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Update and rebuild
docker-compose up --build -d
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
python run_local.py

# Run tests (if available)
python -m pytest
```

## 📁 Project Structure

```
Stablecoin-Tracker-Dashboard/
├── app.py                 # Main Dash application
├── data_collectors.py     # Data collection modules
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker container definition
├── docker-compose.yml   # Multi-service deployment
├── nginx.conf          # Nginx reverse proxy config
├── deploy.sh           # Automated deployment script
├── run_local.py        # Local development runner
├── env.example         # Environment variables template
└── README.md           # This file
```

## 🔒 Security Features

- Rate limiting on API endpoints
- SSL/TLS encryption with nginx
- Security headers implementation
- Non-root Docker container execution
- Environment variable protection

## 📈 Monitoring & Health Checks

- Built-in health check endpoints
- Docker health checks
- Automatic restart on failure
- Comprehensive logging
- Error handling and recovery

## 🚀 Deployment Options

### 1. Docker Compose (Recommended)
- Easy setup and management
- Production-ready configuration
- SSL termination with nginx
- Health monitoring

### 2. Local Development
- Fast iteration and debugging
- Direct access to all components
- Easy testing and modification

### 3. Cloud Deployment
- Compatible with AWS, GCP, Azure
- Kubernetes deployment ready
- Horizontal scaling support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Create an issue in the repository
- Check the logs: `docker-compose logs -f`
- Verify API keys and configuration
- Ensure all dependencies are installed

## 🔮 Future Enhancements

- [ ] Additional stablecoin support
- [ ] Advanced anomaly detection algorithms
- [ ] Alert system and notifications
- [ ] Data export and reporting
- [ ] Mobile app companion
- [ ] Multi-chain support
- [ ] Historical data storage
- [ ] API rate limit optimization

---

**Built with ❤️ using Python, Dash, Plotly, and modern web technologies**