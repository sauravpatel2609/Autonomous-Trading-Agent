import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import os

# Determine the absolute path for the model file
# This ensures the path is correct regardless of where the script is run from
_MODEL_DIR = os.path.dirname(__file__)
_DEFAULT_MODEL_PATH = os.path.join(_MODEL_DIR, "stock_model.pkl")

def train_model(data: pd.DataFrame, model_path: str = _DEFAULT_MODEL_PATH):
    """
    Trains a RandomForestRegressor model and saves it to a file.

    Args:
        data (pd.DataFrame): The preprocessed data with features and a target.
        model_path (str): The path to save the trained model file.
    """
    # 1. Define features (X) and target (y)
    # Our features are all columns that start with 'feature_'
    features = [col for col in data.columns if 'feature_' in col]
    target = 'target_return'
    
    X = data[features]
    y = data[target]
    
    # 2. Split data into training and testing sets
    # For time-series data, it's crucial NOT to shuffle the data.
    # We train on the past (older data) and test on the near future (newer data).
    # test_size=0.2 means we'll use the latest 20% of the data for testing.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )
    
    print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples.")
    
    # 3. Initialize and train the model
    # n_estimators=100 means the model is built from 100 "decision trees".
    # random_state=42 ensures we get the same result every time we run it.
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # 4. Evaluate the model
    # We make predictions on the test set (data the model has never seen).
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Model Mean Squared Error on Test Data: {mse:.4f}")
    
    # 5. Save the trained model
    joblib.dump(model, model_path)
    print(f"✅ Model successfully trained and saved to {model_path}")
    
    return model