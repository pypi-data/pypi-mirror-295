import pandas as pd
import numpy as np
import pandas_ta as ta
import joblib
from sklearn.preprocessing import MinMaxScaler

# Load the data
data = pd.read_csv('eth_price_data.csv')
data.set_index('timestamp', inplace=True)

# Convert 'close' to numeric
data['close'] = pd.to_numeric(data['close'], errors='coerce')

# Add more features: RSI, MA (moving averages), MACD
data['RSI'] = ta.rsi(data['close'], length=14)
data['MA_20'] = ta.sma(data['close'], length=20)
data['MACD'], data['MACD_signal'], _ = ta.macd(data['close'])

# Drop rows with NaN values from the indicators and ensure all columns are numeric
data = data.dropna()

# Ensure all columns are numeric
data[['close', 'RSI', 'MA_20', 'MACD']] = data[['close', 'RSI', 'MA_20', 'MACD']].apply(pd.to_numeric, errors='coerce')

# Initialize and fit the MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data[['close', 'RSI', 'MA_20', 'MACD']])

# Save the MinMaxScaler object for later use
joblib.dump(scaler, 'scaler_custom.pkl')

# Create the time-series dataset
def create_dataset(data, time_step=60):
    X, Y = [], []
    for i in range(len(data)-time_step-1):
        X.append(data[i:(i+time_step), :])  # Use all features (price + indicators)
        Y.append(data[i + time_step, 0])  # Predict the price (close)
    return np.array(X), np.array(Y)

time_step = 20  # You can modify this to control how much past data is used for prediction
X, Y = create_dataset(scaled_data, time_step)

# Reshape data to be [samples, time steps, features]
X = X.reshape(X.shape[0], X.shape[1], X.shape[2])

# Save the datasets
np.save('X.npy', X)
np.save('Y.npy', Y)

print("Preprocessing complete and data saved.")
