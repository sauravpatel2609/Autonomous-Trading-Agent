# run_training.py
from src.data_fetch import fetch_yfinance
from src.preprocessing import create_features
from src.train_model import train_model
import pandas as pd

if __name__ == "__main__":
    # 1. Fetch a good amount of historical data
    print("Fetching historical data for training...")
    # Using a well-known stable ticker like SPY (S&P 500 ETF) is a good start
    raw_data = fetch_yfinance("SPY", period="5y", interval="1d")

    if raw_data is None or raw_data.empty:
        print("Failed to fetch training data. Exiting.")
    else:
        # 2. Preprocess the data and create features
        print("Creating features...")
        featured_data = create_features(raw_data)
        
        # 3. Train the model
        print("Training the model...")
        train_model(featured_data)
        
        print("\n--- Training complete! ---")
        print("The model has been retrained to predict returns and saved to src/stock_model.pkl")
        print("You can now restart the FastAPI application.")
