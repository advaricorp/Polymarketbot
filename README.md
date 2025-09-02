# 🚀 Polymarket Trading Bot

<div align="center">

![Polymarket Bot](https://img.shields.io/badge/Polymarket-Trading%20Bot-blue?style=for-the-badge&logo=ethereum)
![Python](https://img.shields.io/badge/Python-3.9+-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-0.1.0-orange?style=for-the-badge)

**Advanced AI-Powered Trading Bot for Polymarket Prediction Markets**

[English](#english) | [Español](#español) | [Français](#français)

</div>

---

## 🌍 Multi-Language Support

- [**English**](#english) - Complete documentation
- [**Español**](#español) - Documentación completa
- [**Français**](#français) - Documentation complète

---

## 🇺🇸 English

### 📋 Table of Contents

- [Business Overview](#business-overview)
- [Technical Architecture](#technical-architecture)
- [Features & Capabilities](#features--capabilities)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Usage & Deployment](#usage--deployment)
- [API Documentation](#api-documentation)
- [Security & Compliance](#security--compliance)
- [Contributing](#contributing)
- [Support & Community](#support--community)

### 🎯 Business Overview

**Polymarket Trading Bot** is a cutting-edge, enterprise-grade automated trading solution designed for Polymarket's prediction markets. Built with institutional-grade architecture, this bot leverages advanced AI/ML algorithms to provide sophisticated market analysis, risk management, and automated execution capabilities.

#### 🏢 Target Market
- **Institutional Traders**: Hedge funds, trading firms, and professional investors
- **Retail Traders**: Individual traders seeking automated solutions
- **Market Makers**: Liquidity providers and arbitrage traders
- **Research Institutions**: Academic and commercial research organizations

#### 💼 Business Value Proposition
- **Automated Trading**: 24/7 market monitoring and execution
- **AI-Powered Analysis**: Advanced sentiment and technical analysis
- **Risk Management**: Sophisticated position sizing and portfolio protection
- **Scalability**: Microservices architecture for enterprise deployment
- **Compliance**: Built-in regulatory compliance and audit trails

#### 📊 Market Opportunity
- **Prediction Markets Growth**: Expanding global prediction market ecosystem
- **DeFi Adoption**: Increasing institutional interest in decentralized finance
- **AI Integration**: Growing demand for AI-powered trading solutions
- **Regulatory Clarity**: Improving regulatory framework for crypto trading

### 🏗️ Technical Architecture

#### System Overview
The bot implements a **microservices architecture** with event-driven design, ensuring high availability, scalability, and maintainability.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI  │    │   Mobile App   │    │   API Gateway   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API Gateway                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │   Auth     │ │   Rate     │ │   Load     │ │   Caching   │ │
│  │  Service   │ │  Limiting  │ │ Balancing  │ │   Layer     │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Core Trading Services                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │   Data     │ │   Market    │ │   Decision  │ │   Order     │ │
│  │ Ingestion  │ │  Analysis   │ │   Logic     │ │ Execution   │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │ PostgreSQL │ │    Redis    │ │  ChromaDB   │ │   Logging   │ │
│  │  Database  │ │   Cache     │ │ Vector DB   │ │  & Metrics  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

#### Core Services

##### 1. **Data Ingestion Service** (`services/ingest/`)
- **WebSocket Integration**: Real-time market data from Polymarket
- **News API Integration**: External news and sentiment data
- **Data Validation**: Schema validation and data quality checks
- **Rate Limiting**: Intelligent rate limiting and backoff strategies

##### 2. **Market Analysis Service** (`services/analysis/`)
- **Technical Analysis**: Advanced chart patterns and indicators
- **Sentiment Analysis**: LLM-powered news and social media analysis
- **Volatility Modeling**: GARCH and stochastic volatility models
- **Market Microstructure**: Order book analysis and liquidity metrics

##### 3. **Decision Logic Service** (`services/decision/`)
- **Strategy Engine**: Multi-strategy framework with backtesting
- **Risk Management**: VaR, position sizing, and portfolio optimization
- **Signal Generation**: Multi-factor signal aggregation
- **Performance Analytics**: Real-time P&L and performance metrics

##### 4. **Order Execution Service** (`services/execution/`)
- **Order Management**: Smart order routing and execution
- **Position Tracking**: Real-time position and P&L monitoring
- **Slippage Control**: Advanced execution algorithms
- **Compliance Engine**: Regulatory compliance and audit trails

##### 5. **Monitoring Service** (`services/monitoring/`)
- **Real-time Dashboard**: Web-based monitoring interface
- **Alerting System**: Configurable alerts and notifications
- **Performance Metrics**: Comprehensive trading performance analytics
- **System Health**: Infrastructure monitoring and health checks

### 🚀 Features & Capabilities

#### Core Trading Features
- ✅ **Real-time Market Data**: WebSocket-based live market feeds
- ✅ **AI-Powered Analysis**: Advanced LLM integration for market insights
- ✅ **Multi-Strategy Support**: Configurable trading strategies
- ✅ **Risk Management**: Sophisticated position sizing and portfolio protection
- ✅ **Automated Execution**: Intelligent order routing and execution
- ✅ **Performance Analytics**: Comprehensive P&L and performance tracking

#### Advanced Capabilities
- 🔥 **Sentiment Analysis**: Real-time news and social media sentiment
- 🔥 **Technical Indicators**: 50+ technical analysis indicators
- 🔥 **Portfolio Optimization**: Modern portfolio theory implementation
- 🔥 **Backtesting Engine**: Historical strategy performance analysis
- 🔥 **Machine Learning**: Predictive modeling and pattern recognition
- 🔥 **API Integration**: RESTful API for external integrations

#### Enterprise Features
- 🏢 **Multi-User Support**: Role-based access control
- 🏢 **Audit Logging**: Comprehensive audit trail and compliance
- 🏢 **Scalability**: Horizontal scaling and load balancing
- 🏢 **High Availability**: Fault tolerance and disaster recovery
- 🏢 **Monitoring**: Advanced monitoring and alerting systems
- 🏢 **Documentation**: Comprehensive API and user documentation

### 📦 Installation & Setup

#### Prerequisites
- **Python**: 3.9 or higher
- **PostgreSQL**: 13 or higher
- **Redis**: 6.0 or higher
- **Node.js**: 16 or higher (for frontend)
- **Docker**: 20.10 or higher (recommended)

#### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/advaricorp/Polymarketbot.git
cd Polymarketbot

# Start with Docker Compose
docker-compose up -d

# Access the dashboard
open http://localhost:3000
```

#### Manual Installation

```bash
# Clone the repository
git clone https://github.com/advaricorp/Polymarketbot.git
cd Polymarketbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your credentials

# Initialize database
python init_db.py

# Start services
python services/ingest/main.py
```

### ⚙️ Configuration

#### Environment Variables

```bash
# Polymarket API Configuration
POLY_API_KEY=your_api_key
POLY_API_SECRET=your_api_secret
POLY_PASSPHRASE=your_passphrase

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/polymarketbot
REDIS_URL=redis://localhost:6379

# Trading Configuration
TRADING_ENABLED=true
RISK_LIMIT_PERCENT=5.0
MAX_POSITION_SIZE=1000

# AI/ML Configuration
OPENAI_API_KEY=your_openai_key
SENTIMENT_ANALYSIS_ENABLED=true

# Monitoring Configuration
LOG_LEVEL=INFO
METRICS_ENABLED=true
ALERT_EMAIL=alerts@yourcompany.com
```

#### Trading Strategy Configuration

```yaml
# config/strategies.yaml
strategies:
  momentum:
    enabled: true
    parameters:
      lookback_period: 20
      threshold: 0.02
      max_position_size: 0.1
  
  mean_reversion:
    enabled: true
    parameters:
      window_size: 50
      std_dev_threshold: 2.0
      reversion_strength: 0.5
```

### 🚀 Usage & Deployment

#### Development Mode

```bash
# Start development environment
./start_dev.sh

# Run tests
pytest tests/

# Start individual services
python services/ingest/main.py
python services/analysis/main.py
python services/decision/main.py
python services/execution/main.py
```

#### Production Deployment

```bash
# Build production images
docker build -t polymarketbot:latest .

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Monitor deployment
docker-compose logs -f
```

#### Service Management

```bash
# Check service status
./scripts/health_check.sh

# Restart services
./scripts/restart_services.sh

# Backup database
./scripts/backup_db.sh
```

### 📚 API Documentation

#### REST API Endpoints

```bash
# Market Data
GET /api/v1/markets          # List all markets
GET /api/v1/markets/{id}     # Get market details
GET /api/v1/markets/{id}/trades  # Get market trades

# Trading Operations
POST /api/v1/orders          # Place order
GET /api/v1/orders           # List orders
DELETE /api/v1/orders/{id}   # Cancel order

# Portfolio Management
GET /api/v1/portfolio        # Get portfolio overview
GET /api/v1/positions        # List open positions
GET /api/v1/pnl              # Get P&L data

# Analytics
GET /api/v1/analytics/performance  # Performance metrics
GET /api/v1/analytics/risk         # Risk metrics
GET /api/v1/analytics/sentiment    # Sentiment analysis
```

#### WebSocket API

```javascript
// Connect to WebSocket
const ws = new WebSocket('wss://api.polymarketbot.com/ws');

// Subscribe to market updates
ws.send(JSON.stringify({
  action: 'subscribe',
  channel: 'market_data',
  market_id: 'market_123'
}));

// Handle market updates
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Market update:', data);
};
```

### 🔒 Security & Compliance

#### Security Features
- **Encryption**: AES-256 encryption for sensitive data
- **Authentication**: JWT-based authentication with refresh tokens
- **Authorization**: Role-based access control (RBAC)
- **API Security**: Rate limiting and DDoS protection
- **Audit Logging**: Comprehensive security event logging

#### Compliance Features
- **Regulatory Compliance**: Built-in compliance with financial regulations
- **Data Privacy**: GDPR and CCPA compliance
- **Audit Trails**: Complete audit trail for all operations
- **Reporting**: Automated regulatory reporting capabilities
- **KYC/AML**: Integration with KYC/AML verification services

#### Best Practices
- **Secret Management**: Secure credential storage and rotation
- **Network Security**: VPC isolation and firewall rules
- **Monitoring**: Real-time security monitoring and alerting
- **Incident Response**: Automated incident detection and response
- **Backup & Recovery**: Automated backup and disaster recovery

### 🤝 Contributing

We welcome contributions from the community! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

#### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/your-username/Polymarketbot.git
cd Polymarketbot

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes and commit
git add .
git commit -m "Add amazing feature"

# Push to branch
git push origin feature/amazing-feature

# Create pull request
```

#### Code Standards
- **Python**: Follow PEP 8 style guidelines
- **Type Hints**: Use type hints for all functions
- **Documentation**: Comprehensive docstrings and comments
- **Testing**: Minimum 90% test coverage
- **Linting**: Pass all linting checks

### 📞 Support & Community

#### Getting Help
- **Documentation**: [Full Documentation](https://docs.polymarketbot.com)
- **Issues**: [GitHub Issues](https://github.com/advaricorp/Polymarketbot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/advaricorp/Polymarketbot/discussions)
- **Email**: support@polymarketbot.com

#### Community Resources
- **Discord**: [Join our Discord](https://discord.gg/polymarketbot)
- **Telegram**: [Telegram Channel](https://t.me/polymarketbot)
- **Twitter**: [Follow us](https://twitter.com/polymarketbot)
- **Blog**: [Technical Blog](https://blog.polymarketbot.com)

#### Enterprise Support
- **24/7 Support**: Round-the-clock technical support
- **Custom Development**: Custom features and integrations
- **Training**: Team training and certification programs
- **Consulting**: Strategic consulting and implementation services

---

## 🇪🇸 Español

### 📋 Tabla de Contenidos

- [Visión General del Negocio](#visión-general-del-negocio)
- [Arquitectura Técnica](#arquitectura-técnica)
- [Características y Capacidades](#características-y-capacidades)
- [Instalación y Configuración](#instalación-y-configuración)
- [Configuración](#configuración-1)
- [Uso y Despliegue](#uso-y-despliegue)
- [Documentación de la API](#documentación-de-la-api)
- [Seguridad y Cumplimiento](#seguridad-y-cumplimiento)
- [Contribuciones](#contribuciones)
- [Soporte y Comunidad](#soporte-y-comunidad)

### 🎯 Visión General del Negocio

**Polymarket Trading Bot** es una solución de trading automatizado de clase empresarial diseñada para los mercados de predicción de Polymarket. Construido con arquitectura de nivel institucional, este bot aprovecha algoritmos avanzados de IA/ML para proporcionar análisis de mercado sofisticado, gestión de riesgos y capacidades de ejecución automatizada.

#### 🏢 Mercado Objetivo
- **Traders Institucionales**: Fondos de cobertura, firmas de trading e inversores profesionales
- **Traders Minoristas**: Traders individuales que buscan soluciones automatizadas
- **Market Makers**: Proveedores de liquidez y traders de arbitraje
- **Instituciones de Investigación**: Organizaciones de investigación académica y comercial

#### 💼 Propuesta de Valor Comercial
- **Trading Automatizado**: Monitoreo y ejecución del mercado 24/7
- **Análisis Impulsado por IA**: Análisis avanzado de sentimiento y técnico
- **Gestión de Riesgos**: Tamaño de posición sofisticado y protección de portafolio
- **Escalabilidad**: Arquitectura de microservicios para despliegue empresarial
- **Cumplimiento**: Cumplimiento regulatorio integrado y auditorías

### 🏗️ Arquitectura Técnica

#### Visión General del Sistema
El bot implementa una **arquitectura de microservicios** con diseño dirigido por eventos, asegurando alta disponibilidad, escalabilidad y mantenibilidad.

#### Servicios Principales

##### 1. **Servicio de Ingesta de Datos** (`services/ingest/`)
- **Integración WebSocket**: Datos de mercado en tiempo real de Polymarket
- **Integración de API de Noticias**: Datos externos de noticias y sentimiento
- **Validación de Datos**: Validación de esquema y verificaciones de calidad de datos
- **Limitación de Tasa**: Estrategias inteligentes de limitación de tasa y retroceso

##### 2. **Servicio de Análisis de Mercado** (`services/analysis/`)
- **Análisis Técnico**: Patrones de gráficos avanzados e indicadores
- **Análisis de Sentimiento**: Análisis de noticias y redes sociales impulsado por LLM
- **Modelado de Volatilidad**: Modelos GARCH y de volatilidad estocástica
- **Microestructura del Mercado**: Análisis del libro de órdenes y métricas de liquidez

### 🚀 Características y Capacidades

#### Características Principales de Trading
- ✅ **Datos de Mercado en Tiempo Real**: Alimentaciones de mercado en vivo basadas en WebSocket
- ✅ **Análisis Impulsado por IA**: Integración avanzada de LLM para insights del mercado
- ✅ **Soporte Multi-Estrategia**: Estrategias de trading configurables
- ✅ **Gestión de Riesgos**: Tamaño de posición sofisticado y protección de portafolio
- ✅ **Ejecución Automatizada**: Enrutamiento inteligente de órdenes y ejecución
- ✅ **Analíticas de Rendimiento**: Seguimiento integral de P&L y rendimiento

### 📦 Instalación y Configuración

#### Requisitos Previos
- **Python**: 3.9 o superior
- **PostgreSQL**: 13 o superior
- **Redis**: 6.0 o superior
- **Node.js**: 16 o superior (para frontend)
- **Docker**: 20.10 o superior (recomendado)

#### Inicio Rápido con Docker

```bash
# Clonar el repositorio
git clone https://github.com/advaricorp/Polymarketbot.git
cd Polymarketbot

# Iniciar con Docker Compose
docker-compose up -d

# Acceder al dashboard
open http://localhost:3000
```

### ⚙️ Configuración

#### Variables de Entorno

```bash
# Configuración de API de Polymarket
POLY_API_KEY=tu_clave_api
POLY_API_SECRET=tu_secreto_api
POLY_PASSPHRASE=tu_frase_contraseña

# Configuración de Base de Datos
DATABASE_URL=postgresql://usuario:contraseña@localhost/polymarketbot
REDIS_URL=redis://localhost:6379

# Configuración de Trading
TRADING_ENABLED=true
RISK_LIMIT_PERCENT=5.0
MAX_POSITION_SIZE=1000
```

### 🔒 Seguridad y Cumplimiento

#### Características de Seguridad
- **Encriptación**: Encriptación AES-256 para datos sensibles
- **Autenticación**: Autenticación basada en JWT con tokens de actualización
- **Autorización**: Control de acceso basado en roles (RBAC)
- **Seguridad de API**: Limitación de tasa y protección DDoS
- **Registro de Auditoría**: Registro integral de eventos de seguridad

---

## 🇫🇷 Français

### 📋 Table des Matières

- [Aperçu Commercial](#aperçu-commercial)
- [Architecture Technique](#architecture-technique)
- [Fonctionnalités et Capacités](#fonctionnalités-et-capacités)
- [Installation et Configuration](#installation-et-configuration)
- [Configuration](#configuration-2)
- [Utilisation et Déploiement](#utilisation-et-déploiement)
- [Documentation de l'API](#documentation-de-lapi)
- [Sécurité et Conformité](#sécurité-et-conformité)
- [Contributions](#contributions)
- [Support et Communauté](#support-et-communauté)

### 🎯 Aperçu Commercial

**Polymarket Trading Bot** est une solution de trading automatisé de niveau entreprise conçue pour les marchés de prédiction de Polymarket. Construit avec une architecture de niveau institutionnel, ce bot exploite des algorithmes avancés d'IA/ML pour fournir une analyse de marché sophistiquée, une gestion des risques et des capacités d'exécution automatisée.

#### 🏢 Marché Cible
- **Traders Institutionnels**: Fonds de couverture, sociétés de trading et investisseurs professionnels
- **Traders Particuliers**: Traders individuels recherchant des solutions automatisées
- **Market Makers**: Fournisseurs de liquidité et traders d'arbitrage
- **Institutions de Recherche**: Organisations de recherche académique et commerciale

#### 💼 Proposition de Valeur Commerciale
- **Trading Automatisé**: Surveillance et exécution du marché 24/7
- **Analyse Propulsée par l'IA**: Analyse avancée du sentiment et technique
- **Gestion des Risques**: Dimensionnement sophistiqué des positions et protection du portefeuille
- **Évolutivité**: Architecture de microservices pour le déploiement entreprise
- **Conformité**: Conformité réglementaire intégrée et pistes d'audit

### 🏗️ Architecture Technique

#### Vue d'Ensemble du Système
Le bot implémente une **architecture de microservices** avec une conception pilotée par les événements, assurant une haute disponibilité, une évolutivité et une maintenabilité.

#### Services Principaux

##### 1. **Service d'Ingestion de Données** (`services/ingest/`)
- **Intégration WebSocket**: Données de marché en temps réel de Polymarket
- **Intégration de l'API d'Actualités**: Données externes d'actualités et de sentiment
- **Validation des Données**: Validation de schéma et vérifications de qualité des données
- **Limitation de Débit**: Stratégies intelligentes de limitation de débit et de retrait

##### 2. **Service d'Analyse de Marché** (`services/analysis/`)
- **Analyse Technique**: Modèles de graphiques avancés et indicateurs
- **Analyse du Sentiment**: Analyse des actualités et des réseaux sociaux propulsée par LLM
- **Modélisation de la Volatilité**: Modèles GARCH et de volatilité stochastique
- **Microstructure du Marché**: Analyse du carnet d'ordres et métriques de liquidité

### 🚀 Fonctionnalités et Capacités

#### Fonctionnalités Principales de Trading
- ✅ **Données de Marché en Temps Réel**: Flux de marché en direct basés sur WebSocket
- ✅ **Analyse Propulsée par l'IA**: Intégration avancée de LLM pour les insights du marché
- ✅ **Support Multi-Stratégie**: Stratégies de trading configurables
- ✅ **Gestion des Risques**: Dimensionnement sophistiqué des positions et protection du portefeuille
- ✅ **Exécution Automatisée**: Routage intelligent des ordres et exécution
- ✅ **Analyses de Performance**: Suivi complet du P&L et de la performance

### 📦 Installation et Configuration

#### Prérequis
- **Python**: 3.9 ou supérieur
- **PostgreSQL**: 13 ou supérieur
- **Redis**: 6.0 ou supérieur
- **Node.js**: 16 ou supérieur (pour le frontend)
- **Docker**: 20.10 ou supérieur (recommandé)

#### Démarrage Rapide avec Docker

```bash
# Cloner le dépôt
git clone https://github.com/advaricorp/Polymarketbot.git
cd Polymarketbot

# Démarrer avec Docker Compose
docker-compose up -d

# Accéder au tableau de bord
open http://localhost:3000
```

### ⚙️ Configuration

#### Variables d'Environnement

```bash
# Configuration de l'API Polymarket
POLY_API_KEY=votre_clé_api
POLY_API_SECRET=votre_secret_api
POLY_PASSPHRASE=votre_phrase_secrète

# Configuration de la Base de Données
DATABASE_URL=postgresql://utilisateur:mot_de_passe@localhost/polymarketbot
REDIS_URL=redis://localhost:6379

# Configuration du Trading
TRADING_ENABLED=true
RISK_LIMIT_PERCENT=5.0
MAX_POSITION_SIZE=1000
```

### 🔒 Sécurité et Conformité

#### Fonctionnalités de Sécurité
- **Chiffrement**: Chiffrement AES-256 pour les données sensibles
- **Authentification**: Authentification basée sur JWT avec tokens de rafraîchissement
- **Autorisation**: Contrôle d'accès basé sur les rôles (RBAC)
- **Sécurité de l'API**: Limitation de débit et protection DDoS
- **Journalisation d'Audit**: Journalisation complète des événements de sécurité

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**IMPORTANT**: This software is for educational and research purposes only. Trading cryptocurrencies and other assets carries significant risks. Users should:

- Conduct thorough research before using this software
- Understand the risks involved in automated trading
- Ensure compliance with all applicable laws and regulations
- Never invest more than they can afford to lose
- Consider consulting with financial advisors

The developers and contributors are not responsible for any financial losses incurred through the use of this software.

---

<div align="center">

**Built with ❤️ by Adrian V**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/advaricorp/Polymarketbot)
[![Discord](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/polymarketbot)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/polymarketbot)

</div>
