import os
from pathlib import Path
import ccxt
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib 
import pandas_ta as ta  # For technical indicators like ATR

base_dir = Path(__file__).resolve().parent
model = os.path.join(base_dir, 'eth_lstm_best_strong_greatest_model.h5')
scaler = os.path.join(base_dir, 'scaler_custom.pkl')

# Initialize Binance API
binance = ccxt.binance()

# Function to fetch the current price
def fetch_current_price(symbol):
    try:
        ticker = binance.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        print(f"Error fetching current price: {str(e)}")
        return None

# Function to fetch historical OHLCV data
def fetch_ohlcv(symbol, timeframe='1h', limit=500):
    try:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"Error fetching OHLCV data: {str(e)}")
        return None

# Function to fetch the latest 48 close prices in real-time (30-minute intervals)
def fetch_latest_data(symbol='ETH/USDT', timeframe='30m', limit=48):
    try:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
        return np.array([x[4] for x in ohlcv])  # Return the close prices
    except Exception as e:
        print(f"Error fetching latest data: {str(e)}")
        return None

# Function to calculate ATR
def calculate_atr(ohlcv_df, period=14):
    return ta.atr(ohlcv_df['high'], ohlcv_df['low'], ohlcv_df['close'], length=period).iloc[-1]

# Function to calculate support and resistance levels
def calculate_support_resistance(ohlcv_df):
    support_level = ohlcv_df['low'].min()  # Simplistic approach; for a real strategy, use more advanced methods
    resistance_level = ohlcv_df['high'].max()
    return support_level, resistance_level

# Function to calculate average stop loss
def calculate_average_stop_loss(stop_loss_atr, stop_loss_sr):
    return (stop_loss_atr + stop_loss_sr) / 2

def show_live_price():
    symbol = 'ETH/USDT'
    
    # Fetch current price
    current_price = fetch_current_price(symbol)
    if current_price is not None:
        print(f"\nLive Ethereum Price: ${round(current_price, 2)}")
    else:
        print("Unable to fetch the current price.")

def make_prediction_and_suggest_stop_loss():
    symbol = 'ETH/USDT'
    
    # Fetch current price
    current_price = fetch_current_price(symbol)
    if current_price is None:
        print("Unable to fetch the current price. Exiting.")
        return
    
    # Fetch the latest 48 data points (30-minute intervals)
    latest_data = fetch_latest_data(symbol=symbol, timeframe='30m', limit=48)
    if latest_data is None or len(latest_data) < 48:
        print('Not enough data to make a prediction. Exiting.')
        return
    
    # Preprocess the data
    latest_data = latest_data.reshape(-1, 1)
    latest_data_scaled = scaler.transform(latest_data)
    latest_data_scaled = latest_data_scaled.reshape(1, latest_data_scaled.shape[0], 1)
    
    # Make prediction
    prediction = model.predict(latest_data_scaled)
    predicted_price_1h_ahead = scaler.inverse_transform(prediction).flatten()[0]
    
    # Calculate the percentage change
    percentage_change = ((predicted_price_1h_ahead - current_price) / current_price) * 100
    
    # Calculate stop loss: Current price minus the difference between predicted and current price
    if predicted_price_1h_ahead > current_price:
        stop_loss = current_price - abs(predicted_price_1h_ahead - current_price)
    else:
        stop_loss = current_price + abs(predicted_price_1h_ahead - current_price)
    
    # Fetch historical data to calculate support/resistance levels
    ohlcv_df = fetch_ohlcv(symbol)
    if ohlcv_df is None:
        print("Unable to fetch OHLCV data. Exiting.")
        return

    support_level, resistance_level = calculate_support_resistance(ohlcv_df)

    # Determine Buy/Sell suggestion
    if percentage_change > 0.5 and predicted_price_1h_ahead:
        suggestion = "\033[92mSuggested Buy\033[0m"  # Green text
    elif percentage_change < -0.5 and predicted_price_1h_ahead:
        suggestion = "\033[93mSuggested Sell\033[0m"  # Orange text
    elif 0.2 <= percentage_change <= 0.5:
        suggestion = "\033[92mShort Buy\033[0m"
    elif -0.5 <= percentage_change <= -0.2:
        suggestion = "\033[93mShort Sell\033[0m"
    elif -0.19 <= percentage_change <= 0.19:
        suggestion = "\033[90mNEUTRAL\033[0m"
    else:
        suggestion = "No strong suggestion"

    # Print the outputs including the stop loss, prediction, and live price
    print(f"\nLive Ethereum Price: ${round(current_price, 2)}")
    print(f"Predicted Price in 1 Hour: ${round(predicted_price_1h_ahead, 2)}")
    print(f"Predicted Percentage Change: {round(percentage_change, 2)}%")
    print(f"Suggested Stop Loss: ${round(stop_loss, 2)}")
    print(f"Support Level: ${round(support_level, 2)}")
    print(f"Resistance Level: ${round(resistance_level, 2)}")
    print(suggestion)

def calculator():
    print("Entering calculator mode. Type 'exitc' to quit.")
    while True:
        user_input = input("Enter a mathematical expression (e.g., 2 + 2): ").strip().lower()
        if user_input == 'exitc':
            print("Exiting calculator mode.")
            break
        try:
            result = eval(user_input)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

def main():
    print("Type 'predict' to make a prediction, 'calculator' to use the calculator, or 'exit' to quit.")

    while True:
        user_input = input("\nEnter command: ").strip().lower()
        
        if user_input == 'pr':
            make_prediction_and_suggest_stop_loss()
        elif user_input == 'calc':
            calculator()
        elif user_input == 'exit':
            print("Exiting...")
            break
        elif user_input == 'p':
            show_live_price()
        else:
            print("Invalid command. Please type 'pr', 'calc', 'p', or 'exit'.")

if __name__ == '__main__':
    main()

#Test 1: $2509.1, Prediction: $2511.00, from $2507.89. ✔ -- ↑
#Test 2: $2516.17, Prediction $2512.68 from $2509.88 ✔ -- ↑
#Test 2: $2563.34, Prediction $2559 from $2553 ✔ -- ↑
#Test 3: $2401.98, Prediction $2396.29 from $2391.0 ✔ -- ↑
#Test 4: $2400.56, Prediction $2400.52 from $2395.75 - 10mins ✔ -- ↑
#Test 5: $2478.48, Prediction $2405.74 from $2398.84 - 180 minutes ✔ ---- outlier -- ↑
#Test 6: $2399.41, Prediction $2457.64 from 2452.57 - 12mins ✔ -- ↑
#Test 7: $2384.00, Prediction $2384.70 from $2393.56 - 13mins ✔ -- ↓
#Test 8: $2383.10, Prediction $2382.97 from $2394.10 - 13mins ✔ -- ↓
#Test 9: $2383.74, Prediction $2381.74 from $2389.13 - 20mins ✔ -- ↓
#Test 10: $2392.50, Prediction $2392 from $2401.14 - 6mins ✔ -- ↓
#Test 11: $2357.50, Prediction $2366.65 from $2371.87 - 26mins ✔ -- ↓
#Test 12: $2367.57, Prediction $2366.45 from $2360.51 - 2mins ✔ -- ↑
#Test 13: $2372, Prediction $2358.87 from $2369.46 - 54mins ✔ -- ↓
#Test 14: $2356, Prediction $2360.97 from $2377.32 - Unknown mins ✔ -- ↓
#Test 15: $2356.12, Prediction $2370.00 from $2400.57 - 40mins ✔ -- ↓
#Test 16: $2340.67, Prediction $2360.69 from $2350.79 - mins x -- ↑
#Test 16: $2340.67, Prediction $2360.69 from $2350.79 - mins x -- ↑