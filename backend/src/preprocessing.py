import pandas as pd
import numpy as np

def create_features(df: pd.DataFrame, window_size: int = 20, is_training: bool = True, for_lstm: bool = False) -> pd.DataFrame:
    """
    Cleans the input DataFrame and engineers features for the model.
    Works with both single ticker and multi-ticker yfinance data.
    Args:
        df (pd.DataFrame): Input data.
        window_size (int): The size of the rolling windows for features.
        is_training (bool): If True, the target variable will be calculated.
                             Set to False when making predictions.
        for_lstm (bool): If True, creates a 'target_next_close' column for LSTM models.
    """
    df = df.copy()

    # --- 0. Standardize column names ---
    # Make all column names title case for consistency
    df.columns = [col.title() for col in df.columns]

    # --- Find and standardize the 'Close' column ---
    close_col_found = None
    # Check for common names, prioritizing adjusted close
    for name in ['Adj Close', 'Close']:
        if name in df.columns:
            close_col_found = name
            break
    
    if not close_col_found:
        # Fallback for other variations
        for col in df.columns:
            if 'close' in col.lower():
                close_col_found = col
                break
        if not close_col_found:
            raise KeyError("Could not find a 'close' price column in the data.")

    # Rename the found column to 'Close' for consistency
    if close_col_found != 'Close':
        df.rename(columns={close_col_found: 'Close'}, inplace=True)
    
    close_col = 'Close'

    # --- 1. Data Cleaning ---
    # Ensure data is numeric before calculations
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df.ffill(inplace=True)
    df.dropna(inplace=True)

    # --- 2. Feature Engineering ---
    df['feature_sma'] = df[close_col].rolling(window=window_size).mean()

    delta = df[close_col].diff()
    gain = (delta.where(delta > 0, 0.0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(window=14).mean()
    
    # Avoid division by zero for RSI
    rs = gain / loss
    rs.replace([np.inf, -np.inf], np.nan, inplace=True)
    rs.fillna(0, inplace=True)

    df['feature_rsi'] = 100 - (100 / (1 + rs))

    roc_shift = df[close_col].shift(window_size)
    # Avoid division by zero for ROC
    roc_shift.replace(0, np.nan, inplace=True)
    df['feature_roc'] = ((df[close_col] - roc_shift) / roc_shift) * 100


    # --- 3. Target Variable (only for training) ---
    if is_training:
        if for_lstm:
            # For LSTM, we want to predict the *actual next closing price*
            df['target_next_close'] = df[close_col].shift(-1)
        else:
            # For the RandomForest model, we predict the *next day's return*
            df['target_return'] = (df[close_col].shift(-1) - df[close_col]) / df[close_col]

    # --- 4. Final Cleanup ---
    df.dropna(inplace=True)

    return df
