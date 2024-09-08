import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler

# Load the data
data = pd.read_csv('LUCY/eth_price_data.csv')
data.set_index('timestamp', inplace=True)

# Convert 'close' to numeric
data['close'] = pd.to_numeric(data['close'], errors='coerce')

# Drop rows with NaN values
data = data.dropna()

# Initialize and fit the MinMaxScaler for 'close' prices only
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data[['close']])  # Fit only on the 'close' price

# Save the MinMaxScaler object for later use
joblib.dump(scaler, 'scaler_custom.pkl')

# Create the time-series dataset
def create_dataset(data, time_step=60):
    X, Y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step), 0])  # Use only the 'close' price
        Y.append(data[i + time_step, 0])  # Predict the 'close' price
    return np.array(X), np.array(Y)

time_step = 20  # Modify this to control how much past data is used for prediction
X, Y = create_dataset(scaled_data, time_step)

# Reshape data to be [samples, time steps, 1 feature]
X = X.reshape(X.shape[0], X.shape[1], 1)

# Save the datasets
np.save('X.npy', X)
np.save('Y.npy', Y)

print("Preprocessing complete and data saved.")
