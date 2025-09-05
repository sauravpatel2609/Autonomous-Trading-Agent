# run_lstm_training.py
from src.data_fetch import fetch_yfinance
from src.preprocessing import create_features
from src.lstm_model import train_lstm_model
import pandas as pd

if __name__ == "__main__":
    # 1. Fetch a good amount of historical data
    print("Fetching historical data for LSTM training...")
    # Using a well-known stable ticker like SPY (S&P 500 ETF) is a good start
    raw_data = fetch_yfinance("SPY", period="5y", interval="1d")

    if raw_data is None or raw_data.empty:
        print("Failed to fetch training data. Exiting.")
    else:
        # 2. Preprocess the data and create features suitable for LSTM
        print("Creating features for LSTM...")
        # The target for LSTM is the next day's closing price
        featured_data = create_features(raw_data, for_lstm=True)
        
        # 3. Train the LSTM model
        print("Training the LSTM model...")
        train_lstm_model(featured_data)
        
        print("\n--- LSTM Training complete! ---")
        print("The model and scalers have been saved to the 'src' directory.")
        print("You can now rebuild the Docker container.")
