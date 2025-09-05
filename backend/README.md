# 🔧 Trading Agent Backend

FastAPI-based backend service for the AI Trading Agent with machine learning predictions and automated trading capabilities.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional)
- Alpaca Trading Account (paper trading)

### Environment Setup

Create a `.env` file in this directory:

```env
# Alpaca API Configuration (Paper Trading)
ALPACA_API_KEY=your_paper_api_key
ALPACA_API_SECRET=your_paper_secret_key

# Database Configuration
MONGODB_URL=mongodb://localhost:27017/trading_db

# JWT Authentication
SECRET_KEY=your_jwt_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Local Development

```bash
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

### Docker Development

```bash
# Start with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t trading-backend .
docker run -p 8000:8000 --env-file .env trading-backend
```

## 📊 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Project Structure

```
backend/
├── src/
│   ├── agent.py              # Trading agent logic
│   ├── api.py                # FastAPI routes
│   ├── auth.py               # JWT authentication
│   ├── backtest.py           # Backtesting functionality
│   ├── config.py             # Configuration settings
│   ├── data_fetch.py         # Market data retrieval
│   ├── db.py                 # Database connections
│   ├── lstm_model.py         # ML model training
│   ├── preprocessing.py      # Data preprocessing
│   ├── schemas.py            # Pydantic models
│   ├── streaming.py          # Real-time data streaming
│   └── train_model.py        # Model training scripts
├── tests/                    # Unit tests
├── notebooks/                # Jupyter notebooks for analysis
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
└── docker-compose.yml      # Multi-service setup
```

## 🤖 AI Trading Agent

### Features
- **LSTM Neural Networks**: Deep learning for price prediction
- **Technical Indicators**: 60+ engineered features
- **Risk Management**: Position sizing and stop-loss
- **Paper Trading**: Safe testing environment
- **Real-time Execution**: Live market data processing

### Usage

```python
# Start agent programmatically
from src.agent import run_agent_loop
import asyncio

# Run for specific ticker
asyncio.run(run_agent_loop("AAPL"))
```

## 📈 Machine Learning Models

### LSTM Model Training

```bash
# Train new LSTM model
python run_lstm_training.py

# Train with custom data
python -m src.train_model --ticker AAPL --days 365
```

### Model Files
- `lstm_model.h5` - Trained LSTM model
- `lstm_scaler_features.pkl` - Feature scaler
- `lstm_scaler_target.pkl` - Target scaler
- `stock_model.pkl` - Alternative ML model

## 🔗 API Endpoints

### Public Endpoints
```
GET  /health                    # Health check
GET  /predict/{ticker}          # ML price prediction
GET  /stock-data/{symbol}       # Historical data
```

### Authentication
```
POST /register                  # User registration
POST /token                     # Login/JWT token
```

### Protected Endpoints
```
GET  /portfolio                 # Portfolio data
GET  /trades                    # Trade history
POST /agent/start               # Start trading agent
POST /agent/stop                # Stop trading agent
GET  /agent/status              # Agent status
WS   /ws/agent-logs            # Real-time logs
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ALPACA_API_KEY` | Alpaca API key | Required |
| `ALPACA_API_SECRET` | Alpaca secret | Required |
| `MONGODB_URL` | MongoDB connection | `mongodb://localhost:27017/trading_db` |
| `SECRET_KEY` | JWT secret | Required |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry | `30` |

### Trading Configuration

Edit `src/config.py` to modify:
- Trading timeframes
- Risk parameters
- Model settings
- API timeouts

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_api.py

# Test trading functions
pytest tests/test_agent.py -v
```

## 📊 Monitoring & Logging

### Real-time Logs
WebSocket endpoint provides live agent activity:
```javascript
// Connect to logs
const ws = new WebSocket('ws://localhost:8000/ws/agent-logs');
ws.onmessage = (event) => console.log(event.data);
```

### Log Levels
- `INFO`: General agent activity
- `WARNING`: Risk alerts and warnings
- `ERROR`: Trading errors and failures
- `SUCCESS`: Successful trades and operations

## 🚀 Deployment

### Production Checklist
- [ ] Set production environment variables
- [ ] Configure production database
- [ ] Set up SSL certificates
- [ ] Configure reverse proxy (nginx)
- [ ] Set up monitoring and alerts
- [ ] Backup strategies for ML models

### Docker Production

```bash
# Build production image
docker build -t trading-backend:prod .

# Run with production config
docker run -d \
  --name trading-backend \
  -p 8000:8000 \
  --env-file .env.prod \
  trading-backend:prod
```

## 📝 Development Notes

### Adding New Features
1. Create feature branch
2. Add endpoints to `src/api.py`
3. Update schemas in `src/schemas.py`
4. Add tests in `tests/`
5. Update documentation

### Model Improvements
- Add more technical indicators
- Implement ensemble methods
- Optimize hyperparameters
- Add feature selection

## ⚠️ Important Notes

- **Paper Trading Only**: Configured for Alpaca paper trading
- **Rate Limits**: Alpaca API has rate limits
- **Market Hours**: Agent only trades during market hours
- **Risk Management**: Always use position sizing and stop-losses

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure proper Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **Database Connection**
   ```bash
   # Check MongoDB is running
   mongosh --eval "db.runCommand('ping')"
   ```

3. **Alpaca API Issues**
   ```bash
   # Test API connection
   python test_alpaca.py
   ```

4. **Model Loading Errors**
   ```bash
   # Retrain models if corrupted
   python run_lstm_training.py
   ```

## 📞 Support

For issues specific to the backend:
1. Check logs in the terminal
2. Verify environment variables
3. Test API endpoints at `/docs`
4. Review MongoDB connections

### Contact

For technical questions or contributions:
- **Email**: sauravpatel90768@gmail.com
- **GitHub**: [@sauravpatel2609](https://github.com/sauravpatel2609)
- **Issues**: [GitHub Issues](https://github.com/sauravpatel2609/Autonomous-Trading-Agent/issues)

---

**Backend API ready for AI-powered trading! 🚀**
