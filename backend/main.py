from fastapi import FastAPI
from contextlib import asynccontextmanager
import joblib
import os
from tensorflow.keras.models import load_model
from src import api
from src.globals import ml_models
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    Loads the ML model and scalers into memory on startup.
    """
    print("INFO:     Loading LSTM model and scalers...")
    
    _MODEL_DIR = os.path.dirname(__file__)
    model_path = os.path.join(_MODEL_DIR, "src/lstm_model.h5")
    scaler_features_path = os.path.join(_MODEL_DIR, "src/lstm_scaler_features.pkl")
    scaler_target_path = os.path.join(_MODEL_DIR, "src/lstm_scaler_target.pkl")
    
    ml_models['lstm'] = load_model(model_path)
    ml_models['scaler_features'] = joblib.load(scaler_features_path)
    ml_models['scaler_target'] = joblib.load(scaler_target_path)
    
    print("INFO:     LSTM Model and scalers loaded successfully.")
    yield
    
    ml_models.clear()
    print("INFO:     Cleaned up ML models.")

app = FastAPI(lifespan=lifespan, title="Trading Agent API")

# Add CORS middleware to allow the frontend to connect
origins = [
    "http://localhost:3000", # For Create React App
    "http://localhost:5173", # For Vite
    "http://localhost:8080", # Common alternative for Vite
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all the API routes from api.py
app.include_router(api.router)

# Add the health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}