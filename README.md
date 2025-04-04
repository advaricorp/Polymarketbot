# Polymarket Trading Bot

## Overview
An advanced trading bot for Polymarket using AI-powered analysis and automated execution. This bot implements a microservices architecture to handle market data ingestion, analysis, and trade execution on Polymarket's prediction markets.

## Features
- Real-time market data ingestion via WebSocket
- AI-powered news analysis using LLM
- Automated trading strategy execution
- Risk management and position sizing
- Comprehensive monitoring and logging
- Support for both mainnet and testnet (Mumbai)

## Architecture
The bot is built using a microservices architecture with the following components:

1. **Data Ingestion Service**
   - WebSocket connection to Polymarket
   - Real-time market data processing
   - News and external data integration

2. **Market Analysis Service**
   - Volatility and technical analysis
   - LLM-based news analysis
   - Market signal generation

3. **Decision Logic Service**
   - Trading strategy implementation
   - Position sizing and risk management
   - Order generation

4. **Order Execution Service**
   - Order management and execution
   - Position tracking
   - Balance management

5. **Monitoring Service**
   - Real-time performance tracking
   - Logging and alerting
   - Dashboard visualization

## Prerequisites
- Python 3.9+
- PostgreSQL
- Redis
- Node.js (optional, for dashboard)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/advaricorp/Polymarketbot.git
cd Polymarketbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. Create necessary directories:
```bash
mkdir -p data/logs data/vector_db
```

## Configuration

### Required Credentials
1. **Polygon Wallet Setup**:
   - Create a MetaMask wallet
   - Add Polygon network
   - Export private key (securely)

2. **Polymarket API Credentials**:
   - Create Polymarket account
   - Complete KYC verification
   - Generate API credentials

3. **Database Setup**:
   - Configure PostgreSQL
   - Set up Redis
   - Initialize ChromaDB

### Environment Variables
Configure the following in your .env file:
- POLY_PRIVATE_KEY
- POLY_API_KEY
- POLY_API_SECRET
- POLY_PASSPHRASE
- Database URLs
- API endpoints
- Logging configuration

## Usage

1. Start the services:
```bash
python services/ingest/main.py
```

2. Test the connection:
```bash
./services/ingest/test_ws.py
./services/ingest/test_health.sh
```

3. Monitor the dashboard:
```bash
python services/monitor/dashboard.py
```

## Testing
- Use Mumbai testnet for initial testing
- Start with small amounts on mainnet
- Regular testing of all components

## Security Considerations
- Secure credential management
- Regular key rotation
- Proper access controls
- Backup procedures

## Contributing
Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License
[MIT License](LICENSE)

## Disclaimer
This bot is for educational purposes only. Trading carries significant risks. Use at your own risk and ensure compliance with all applicable laws and regulations.
