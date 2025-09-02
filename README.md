# 🚀 AI-Powered Trading Agent

> An intelligent autonomous trading system built with React, FastAccess the application:
- **Frontend**: http://localhost:5173 (or auto-incremented port like 5174 if busy)
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs and LSTM neural networks for algorithmic stock trading.

[![Licen## 📞 Support

If you have any questions or issues, please:
1. Check the [Issues](https://github.com/sauravpatel2609/Autonomous-Trading-Agent/issues) page
2. Create a new issue with detailed information
3. Join our community discussions

## Contact

For security-related questions or general inquiries:
- **Email**: sauravpatel90768@gmail.com
- **GitHub**: [@sauravpatel2609](https://github.com/sauravpatel2609)
- **Project Repository**: [Autonomous-Trading-Agent](https://github.com/sauravpatel2609/Autonomous-Trading-Agent)

---

**Built with ❤️ by Saurav Patel**ttps://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688.svg)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8-3178C6.svg)](https://www.typescriptlang.org/)

## 📊 Overview

This project is a full-stack trading application that combines machine learning predictions with automated trading execution. It features an AI agent that uses LSTM neural networks to predict stock prices and execute trades through the Alpaca API, all managed through a modern React dashboard.

### ✨ Key Features

- 🤖 **Autonomous Trading Agent** - AI-powered decision making with LSTM models
- 📈 **Real-time Stock Analysis** - Live price tracking and technical indicators
- 🎯 **ML-Based Predictions** - Deep learning models for price forecasting
- 💼 **Portfolio Management** - Real-time portfolio tracking and performance metrics
- 🔒 **Secure Authentication** - JWT-based user authentication system
- 📱 **Responsive Dashboard** - Modern React UI with shadcn/ui components
- 🔄 **Live Updates** - WebSocket connections for real-time data streaming
- 📊 **Interactive Charts** - Beautiful data visualization with Recharts
- 🐳 **Docker Support** - Containerized deployment with Docker Compose

## 🏗️ Architecture

```
├── agent-stock-frontend/     # React TypeScript Frontend
├── backend/                  # FastAPI Python Backend
├── docker-compose.yml        # Multi-service orchestration
└── README.md                # This file
```

### Frontend (React + TypeScript)
- **Framework**: Vite + React 18 + TypeScript
- **UI Components**: shadcn/ui + Radix UI
- **Styling**: Tailwind CSS
- **State Management**: TanStack Query
- **Charts**: Recharts + Lightweight Charts
- **Authentication**: JWT tokens

### Backend (FastAPI + Python)
- **API Framework**: FastAPI
- **ML Framework**: TensorFlow/Keras (LSTM)
- **Data Processing**: Pandas + NumPy
- **Trading API**: Alpaca Markets
- **Database**: MongoDB
- **Authentication**: JWT + bcrypt

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Docker** and Docker Compose
- **Alpaca Trading Account** (for API keys)

### 1. Clone the Repository

```bash
git clone https://github.com/sauravpatel2609/Autonomous-Trading-Agent.git
cd Autonomous-Trading-Agent
```

### 2. Environment Setup

Create a `.env` file in the `backend/` directory:

```env
# Alpaca API Configuration
ALPACA_API_KEY=your_alpaca_api_key
ALPACA_API_SECRET=your_alpaca_secret_key

# Database Configuration
MONGODB_URL=mongodb://localhost:27017/trading_db

# JWT Configuration
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Using Docker (Recommended)

```bash
# Start the entire stack
cd backend
docker-compose up --build

# Start frontend separately
cd ../agent-stock-frontend
npm install
npm run dev
```

Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 4. Manual Setup (Development)

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv trading-agent-env
source trading-agent-env/bin/activate  # Linux/Mac
# or
trading-agent-env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload --port 8000
```

#### Frontend Setup

```bash
cd agent-stock-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🤖 AI Trading Agent

The trading agent uses sophisticated machine learning models to make trading decisions:

### LSTM Model Features
- **Deep Learning**: Multi-layer LSTM neural network
- **Technical Indicators**: Moving averages, RSI, MACD, Bollinger Bands
- **Feature Engineering**: 60+ technical and statistical features
- **Time Series**: 60-day lookback window for predictions
- **Real-time Training**: Models retrain with new market data

### Trading Strategy
- **Market Hours**: Only trades during market open hours
- **Risk Management**: Position sizing and stop-loss mechanisms
- **Paper Trading**: Safe testing environment with Alpaca paper account
- **Multi-timeframe**: Supports different trading intervals

## 📊 API Endpoints

### Public Endpoints
- `GET /health` - Health check
- `GET /predict/{ticker}` - Get ML price prediction
- `GET /stock-data/{symbol}` - Historical stock data

### Authentication
- `POST /register` - User registration
- `POST /token` - Login and get JWT token

### Protected Endpoints
- `GET /portfolio` - User's portfolio data
- `GET /trades` - Trading history
- `POST /agent/start` - Start trading agent
- `POST /agent/stop` - Stop trading agent
- `GET /agent/status` - Agent status
- `WebSocket /ws/agent-logs` - Real-time agent logs

## 🎨 Frontend Components

### Main Dashboard
- **Trading Header** - Navigation and user controls
- **Portfolio Component** - Real-time portfolio overview
- **Stock Chart** - Interactive price charts with indicators
- **Prediction Tool** - ML model predictions interface
- **Agent Control** - Start/stop trading agent
- **Trade History** - Transaction history and performance

### UI Features
- **Responsive Design** - Works on desktop and mobile
- **Dark/Light Mode** - Theme switching capability
- **Real-time Updates** - Live data via WebSocket
- **Form Validation** - Zod schema validation
- **Loading States** - Smooth UX with loading indicators

## 🔧 Development

### Project Structure

```
agent-stock-frontend/
├── src/
│   ├── components/
│   │   ├── Auth/           # Authentication components
│   │   ├── trading/        # Trading dashboard components
│   │   └── ui/             # Reusable UI components
│   ├── hooks/              # Custom React hooks
│   ├── lib/                # Utility functions
│   └── pages/              # Page components
├── public/                 # Static assets
└── package.json

backend/
├── src/
│   ├── agent.py           # Trading agent logic
│   ├── api.py             # FastAPI routes
│   ├── auth.py            # Authentication system
│   ├── lstm_model.py      # ML model training
│   ├── preprocessing.py   # Data preprocessing
│   └── config.py          # Configuration
├── main.py                # Application entry point
└── requirements.txt       # Python dependencies
```

### Key Technologies

#### Frontend Stack
- **Vite**: Fast build tool and dev server
- **React Router**: Client-side routing
- **TanStack Query**: Server state management
- **Axios**: HTTP client for API calls
- **shadcn/ui**: Modern component library
- **Tailwind CSS**: Utility-first CSS framework

#### Backend Stack
- **FastAPI**: Modern Python web framework
- **TensorFlow**: Machine learning framework
- **Alpaca**: Trading API integration
- **MongoDB**: Document database
- **WebSockets**: Real-time communication

## 🧪 Testing

### Frontend Testing
```bash
cd agent-stock-frontend
npm run test         # Run unit tests
npm run test:e2e     # Run end-to-end tests
npm run lint         # Code linting
```

### Backend Testing
```bash
cd backend
pytest               # Run Python tests
pytest --cov         # Run with coverage
```

## 🚀 Deployment

### Production Build

```bash
# Frontend
cd agent-stock-frontend
npm run build

# Backend (Docker)
cd backend
docker build -t trading-agent-backend .
```

### Environment Variables (Production)

```env
# Production environment
NODE_ENV=production
ALPACA_API_KEY=your_production_api_key
ALPACA_API_SECRET=your_production_secret
MONGODB_URL=your_production_mongodb_url
SECRET_KEY=your_production_jwt_secret
```

## 📈 Performance & Monitoring

- **API Response Times**: < 200ms for most endpoints
- **ML Prediction Speed**: < 1 second for stock predictions
- **Real-time Updates**: WebSocket latency < 50ms
- **Memory Usage**: Efficient model loading and caching

## 🔐 Security

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: bcrypt for secure password storage
- **CORS Protection**: Configured for frontend origin
- **API Rate Limiting**: Prevents abuse (recommended for production)
- **Environment Variables**: Sensitive data protected

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow TypeScript/Python type hints
- Write tests for new features
- Update documentation for API changes
- Use conventional commit messages

### Quick Start for Contributors

1. **Fork the repository**
   ```bash
   git clone https://github.com/sauravpatel2609/Autonomous-Trading-Agent.git
   cd Autonomous-Trading-Agent
   ```

2. **Setup Backend**
   ```bash
   cd backend
   # Create and activate virtual environment
   python -m venv trading-agent-env
   source trading-agent-env/bin/activate  # Linux/Mac
   # trading-agent-env\Scripts\activate    # Windows
   pip install -r requirements.txt
   ```

3. **Setup Frontend**
   ```bash
   cd agent-stock-frontend
   npm install
   ```

4. **Start Development**
   ```bash
   # Terminal 1: Start backend
   cd backend && docker-compose up --build
   
   # Terminal 2: Start frontend  
   cd agent-stock-frontend && npm run dev
   ```

5. **Access Application**
   - Frontend: http://localhost:5173 (or auto-incremented port)
   - Backend API: http://localhost:8000/docs

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for educational and research purposes only. Trading involves substantial risk of loss and is not suitable for all investors. The developers are not responsible for any financial losses incurred through the use of this software. Always conduct thorough research and consider consulting with financial advisors before making investment decisions.

## 🙏 Acknowledgments

- [Alpaca Markets](https://alpaca.markets/) for trading API
- [shadcn/ui](https://ui.shadcn.com/) for beautiful UI components
- [TensorFlow](https://tensorflow.org/) for machine learning capabilities
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent Python framework

## 📞 Support

If you have any questions or issues, please:
1. Check the [Issues](https://github.com/your-username/your-repo/issues) page
2. Create a new issue with detailed information
3. Join our community discussions

---

**Built with ❤️ by [Saurav]**
