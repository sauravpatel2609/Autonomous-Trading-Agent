# src/backtest.py

import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
import os

def run_backtest(data: pd.DataFrame, model_path: str, initial_capital: float = 10000.0):
    """
    Runs a backtest simulation for a given model and data.

    Args:
        data (pd.DataFrame): The preprocessed data with features.
        model_path (str): Path to the saved model file (.pkl or .h5).
        initial_capital (float): The starting capital for the simulation.

    Returns:
        pd.DataFrame: A DataFrame with backtest results.
    """
    # --- NEW: Standardize column names to Title Case ---
    data.columns = [col.title() for col in data.columns]
    
    # Determine model type from file extension
    if model_path.endswith('.pkl'):
        model = joblib.load(model_path)
        is_lstm = False
    elif model_path.endswith('.h5'):
        model = load_model(model_path)
        # For LSTM, we need the scalers
        _MODEL_DIR = os.path.dirname(__file__)
        scaler_features_path = os.path.join(_MODEL_DIR, "lstm_scaler_features.pkl")
        scaler_target_path = os.path.join(_MODEL_DIR, "lstm_scaler_target.pkl")
        scaler_features = joblib.load(scaler_features_path)
        scaler_target = joblib.load(scaler_target_path)
        is_lstm = True
    else:
        raise ValueError("Unsupported model file type")

    capital = initial_capital
    positions = 0.0
    portfolio_values = []
    trade_log = []

    features = [col for col in data.columns if 'feature_' in col]
    
    for i in range(len(data)):
        current_price = data['Close'].iloc[i]
        
        # --- Prepare features for prediction ---
        if is_lstm:
            # For LSTM, we need the last 60 days of scaled features
            if i < 60:
                portfolio_values.append(capital)
                continue
            
            # Get the last 60 records, scale them, and reshape
            feature_sequence = data[features].iloc[i-60:i]
            scaled_features = scaler_features.transform(feature_sequence)
            input_data = np.reshape(scaled_features, (1, 60, len(features)))
            
            predicted_scaled = model.predict(input_data)
            predicted_price = scaler_target.inverse_transform(predicted_scaled)[0][0]
        else:
            # For RandomForest, we just need the current feature row
            input_data = data[features].iloc[[i]]
            predicted_price = model.predict(input_data)[0]

        # --- Trading Strategy/Logic ---
        # Buy signal: If predicted price is > 2% higher than current price and we have no position
        if predicted_price > current_price * 1.02 and positions == 0:
            positions = capital / current_price
            capital = 0
            trade_log.append(f"BUY at {current_price:.2f} on {data.index[i].date()}")

        # Sell signal: If predicted price is below current price and we have a position
        elif predicted_price < current_price and positions > 0:
            capital = positions * current_price
            positions = 0
            trade_log.append(f"SELL at {current_price:.2f} on {data.index[i].date()}")
        
        # Update portfolio value
        current_portfolio_value = capital + (positions * current_price)
        portfolio_values.append(current_portfolio_value)
    
    results = data.copy()
    results['Portfolio_Value'] = portfolio_values
    
    for log in trade_log:
        print(log)
        
    return results

def calculate_metrics(results: pd.DataFrame):
    """Calculates and prints performance metrics."""
    
    total_return = (results['Portfolio_Value'].iloc[-1] / results['Portfolio_Value'].iloc[0]) - 1
    
    returns = results['Portfolio_Value'].pct_change()
    sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252) # Annualized
    
    rolling_max = results['Portfolio_Value'].cummax()
    daily_drawdown = results['Portfolio_Value'] / rolling_max - 1.0
    max_drawdown = daily_drawdown.min()

    print("\n--- Backtest Performance ---")
    print(f"Total Return: {total_return:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Maximum Drawdown: {max_drawdown:.2%}")
    print("--------------------------")