# src/streaming.py
import logging
from alpaca.data.live import StockDataStream
from src.config import ALPACA_API_KEY, ALPACA_API_SECRET

# Set up basic logging to see output clearly
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# The handler function must be async, as the library runs it in its own event loop
async def trade_handler(data):
    """
    This is the callback function that processes incoming trade data.
    """
    logging.info(f"--- New Trade Received ---")
    logging.info(f"  Symbol: {data.symbol}")
    logging.info(f"  Price: {data.price}")
    logging.info(f"  Volume: {data.size}")
    logging.info(f"  Timestamp: {data.timestamp}")

def main():
    """
    This is the main function to set up and run the stream.
    It is synchronous and the .run() method is blocking.
    """
    TICKER = "AAPL"
    logging.info(f"Subscribing to live trade data for {TICKER}...")

    # 1. Instantiate the client
    stream_client = StockDataStream(
        api_key=ALPACA_API_KEY,
        secret_key=ALPACA_API_SECRET
    )

    # 2. Subscribe to the data stream
    # The async handler function is passed here.
    stream_client.subscribe_trades(trade_handler, TICKER)

    # 3. Run the stream
    # This is a blocking call that will run indefinitely until the script is stopped.
    stream_client.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Stream stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)