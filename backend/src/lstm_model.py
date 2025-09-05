# src/lstm_model.py

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import joblib
import os

# --- NEW: Define absolute paths for saved files ---
_MODEL_DIR = os.path.dirname(__file__)
_DEFAULT_MODEL_PATH = os.path.join(_MODEL_DIR, "lstm_model.h5")
_SCALER_FEATURES_PATH = os.path.join(_MODEL_DIR, "lstm_scaler_features.pkl")
_SCALER_TARGET_PATH = os.path.join(_MODEL_DIR, "lstm_scaler_target.pkl")

def create_sequences(X_data, y_data, time_steps=60):
    """Creates sequences of data for LSTM model."""
    Xs, ys = [], []
    for i in range(len(X_data) - time_steps):
        v = X_data.iloc[i:(i + time_steps)].values
        Xs.append(v)
        ys.append(y_data.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)

def train_lstm_model(data: pd.DataFrame, model_path: str = _DEFAULT_MODEL_PATH):
    """
    Prepares data, builds, trains, and saves an LSTM model.
    """
    # 1. Define features and target, then split data
    features = [col for col in data.columns if 'feature_' in col]
    target = 'target_next_close'
    
    train_size = int(len(data) * 0.8)
    train_df, test_df = data[0:train_size], data[train_size:len(data)]

    # 2. Scale the data
    scaler_features = MinMaxScaler(feature_range=(0, 1))
    scaler_target = MinMaxScaler(feature_range=(0, 1))

    X_train_scaled = scaler_features.fit_transform(train_df[features])
    y_train_scaled = scaler_target.fit_transform(train_df[[target]])
    
    X_test_scaled = scaler_features.transform(test_df[features])
    
    # --- UPDATED: Use the defined paths for saving scalers ---
    joblib.dump(scaler_features, _SCALER_FEATURES_PATH)
    joblib.dump(scaler_target, _SCALER_TARGET_PATH)

    # 3. Create sequences
    TIME_STEPS = 60
    X_train_seq, y_train_seq = create_sequences(
        pd.DataFrame(X_train_scaled), pd.DataFrame(y_train_scaled), TIME_STEPS
    )
    X_test_seq, y_test_seq = create_sequences(
        pd.DataFrame(X_test_scaled), test_df[[target]], TIME_STEPS
    )

    print(f"Training sequence shape: {X_train_seq.shape}")
    print(f"Testing sequence shape: {X_test_seq.shape}")

    # 4. Build the LSTM model
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=(X_train_seq.shape[1], X_train_seq.shape[2])),
        Dropout(0.2),
        LSTM(units=50, return_sequences=False),
        Dropout(0.2),
        Dense(units=25),
        Dense(units=1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.summary()

    # 5. Train the model
    model.fit(X_train_seq, y_train_seq, batch_size=32, epochs=25, validation_split=0.1, verbose=1)

    # 6. Save the trained model
    # --- UPDATED: Use the model_path argument for saving ---
    model.save(model_path)
    print(f"✅ LSTM Model successfully trained and saved to {model_path}")
    
    return model