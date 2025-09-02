#!/bin/bash

# Stablecoin Dashboard Deployment Script
set -e

echo "🚀 Deploying Stablecoin Tracker Dashboard..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create SSL directory and generate self-signed certificate if it doesn't exist
if [ ! -d "./ssl" ]; then
    echo "🔐 Creating SSL directory and generating self-signed certificate..."
    mkdir -p ssl
    openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    echo "✅ SSL certificate generated"
fi

# Create data directory
mkdir -p data

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your API keys before starting the application"
    echo "   You can get API keys from:"
    echo "   - CoinGecko: https://www.coingecko.com/en/api"
    echo "   - Etherscan: https://etherscan.io/apis"
    echo "   - DeFiLlama: https://defillama.com/docs/api"
fi

# Build and start the application
echo "🏗️  Building and starting the application..."
docker-compose up --build -d

# Wait for the application to start
echo "⏳ Waiting for the application to start..."
sleep 30

# Check if the application is running
if curl -f http://localhost:8050/ > /dev/null 2>&1; then
    echo "✅ Dashboard is running successfully!"
    echo ""
    echo "🌐 Access your dashboard at:"
    echo "   - Local: http://localhost:8050"
    echo "   - Nginx: https://localhost (with SSL)"
    echo ""
    echo "📊 Dashboard features:"
    echo "   - Real-time stablecoin price monitoring"
    echo "   - Peg stability analysis"
    echo "   - Supply metrics and on-chain data"
    echo "   - Anomaly detection and alerts"
    echo "   - Interactive charts and visualizations"
    echo ""
    echo "🔧 Management commands:"
    echo "   - View logs: docker-compose logs -f"
    echo "   - Stop: docker-compose down"
    echo "   - Restart: docker-compose restart"
    echo "   - Update: docker-compose up --build -d"
else
    echo "❌ Application failed to start. Check logs with: docker-compose logs"
    exit 1
fi
