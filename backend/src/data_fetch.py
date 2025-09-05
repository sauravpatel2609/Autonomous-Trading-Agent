import yfinance as yf
import requests
import pandas as pd
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from src.config import ALPACA_API_KEY, ALPACA_API_SECRET, POLYGON_API_KEY


# ---- Yahoo Finance ----
def fetch_yfinance(ticker: str, period="1mo", interval="1d"):
    data = yf.download(ticker, period=period, interval=interval)
    
    # Add a check to ensure data is not empty
    if data is None or data.empty:
        print(f"No data found for {ticker} for the given period and interval.")
        return pd.DataFrame() # Return an empty DataFrame

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = ['_'.join(col).strip() for col in data.columns.values]
    # Ensure column names are in Title Case for consistency
    data.columns = [col.title() for col in data.columns]
    return data


# ---- Alpaca API ----
def fetch_alpaca_account():
    """Fetches Alpaca account information using the TradingClient."""
    trading_client = TradingClient(ALPACA_API_KEY, ALPACA_API_SECRET, paper=True)
    return trading_client.get_account()


def fetch_alpaca_data(ticker: str, start: str, end: str):
    """Fetches historical bar data from Alpaca."""
    data_client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_API_SECRET)
    
    request_params = StockBarsRequest(
        symbol_or_symbols=[ticker],
        timeframe=TimeFrame.Day,
        start=pd.to_datetime(start),
        end=pd.to_datetime(end)
    )
    
    barset = data_client.get_stock_bars(request_params)
    return barset.df


# ---- Polygon API ----
def fetch_polygon_data(ticker: str, date: str):
    url = f"https://api.polygon.io/v1/open-close/{ticker}/{date}?adjusted=true&apiKey={POLYGON_API_KEY}"
    resp = requests.get(url)
    return resp.json()
