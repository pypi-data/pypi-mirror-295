import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import joblib

# Define the model file
model_file = 'eth_lstm_model.h5'

# Load the preprocessed datasets and model
X = np.load('X.npy')
Y = np.load('Y.npy')
model = tf.keras.models.load_model(model_file)
scaler = joblib.load('scaler.pkl')

# Split the data into train/test sets
train_size = int(len(Y) * 0.8)
test_data = Y[train_size - 60:]

# Create test datasets
X_test = X[train_size:]
Y_test = Y[train_size:]

# Make predictions
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)

# Plot the results
real_prices = scaler.inverse_transform(Y_test.reshape(-1, 1))

plt.figure(figsize=(14,5))
plt.plot(real_prices, label='Real ETH Price')
plt.plot(predictions, label='Predicted ETH Price')
plt.legend()
plt.show()

# Print the model file used
print(f"Model evaluation complete. Model used: {model_file}")
