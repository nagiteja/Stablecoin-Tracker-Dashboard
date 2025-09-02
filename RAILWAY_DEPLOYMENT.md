# 🚂 Railway Deployment Guide

## Quick Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)

## Manual Deployment Steps

### 1. **Connect to Railway**
1. Go to [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `Stablecoin-Tracker-Dashboard` repository

### 2. **Configure Environment Variables**
In Railway dashboard, go to your project → Variables tab and add:

```
COINGECKO_API_KEY=CG-Rxjdt1pcUyCsvA8tWARNfaVS
ETHERSCAN_API_KEY=5YW8NRUBSS4FQR8411NGV3SUBCGGBXD41W
DEFILLAMA_API_KEY=your_defillama_key_here
DEBUG=False
PORT=8050
```

### 3. **Deploy Settings**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python working_app.py`
- **Port**: Railway will automatically assign (use `$PORT` env var)

### 4. **Domain Configuration**
- Railway will provide a `.railway.app` domain
- You can add a custom domain in the Settings tab

## 🎯 **Deployment Options**

### Option 1: Real-time Data (Recommended)
- Uses `working_app.py`
- Real-time API integration
- Updates every 30 seconds

### Option 2: Static Data (Reliable)
- Uses `simple_app.py` 
- No API dependencies
- Always works

## 🔧 **Railway Configuration Files**

- `railway.json`: Railway-specific configuration
- `Procfile`: Process definition
- `nixpacks.toml`: Build configuration

## 📊 **Monitoring**

Railway provides:
- Real-time logs
- Performance metrics
- Automatic restarts
- Health checks

## 🚀 **After Deployment**

Your dashboard will be available at:
- Railway domain: `https://your-project.railway.app`
- Custom domain (if configured)

## 🔒 **Security Notes**

- API keys are stored as environment variables
- Never commit API keys to GitHub
- Railway automatically handles HTTPS
