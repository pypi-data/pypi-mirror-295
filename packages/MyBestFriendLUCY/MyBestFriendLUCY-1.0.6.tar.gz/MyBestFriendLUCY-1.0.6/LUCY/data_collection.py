import ccxt
import pandas as pd
import time

# Initialize Binance API
binance = ccxt.binance()

# Function to fetch historical data
def fetch_historical_data(symbol, timeframe, since):
    data = []
    while True:
        try:
            ohlcv = binance.fetch_ohlcv(symbol, timeframe, since)
            if len(ohlcv) == 0:
                break
            data.extend(ohlcv)
            since = ohlcv[-1][0] + 1
            time.sleep(0.5)  # Adjust to avoid rate limiting but improve efficiency
        except Exception as e:
            print(f"Error: {str(e)}")
            break
    return data

# Fetch historical data for ETH/USDT
symbol = 'ETH/USDT'
timeframe = '30m'  # 5-minute data for higher frequency
since = binance.parse8601('2023-01-01T00:00:00Z')  # Fetch recent data

ohlcv = fetch_historical_data(symbol, timeframe, since)

# Convert to DataFrame
columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
data = pd.DataFrame(ohlcv, columns=columns)
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
data.set_index('timestamp', inplace=True)

# Save the data to a CSV file
data.to_csv('eth_price_data.csv')
print("Data saved to eth_price_data.csv.")
