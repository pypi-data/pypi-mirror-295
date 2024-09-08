import numpy as np
import tensorflow as tf
import keras_tuner as kt
from tensorflow.keras.models import Sequential  # type: ignore
from tensorflow.keras.layers import LSTM, Dense, Dropout # type: ignore
from tensorflow.keras.callbacks import EarlyStopping # type: ignore

# Load the preprocessed datasets
X = np.load('X.npy')  # Now includes close, RSI, MA, MACD
Y = np.load('Y.npy')

# Define the model
def build_model(hp):
    model = Sequential()
    model.add(LSTM(units=hp.Int('units_1', min_value=50, max_value=200, step=50), 
                   return_sequences=True, input_shape=(X.shape[1], X.shape[2])))  # Adjust input_shape for multi-features
    model.add(Dropout(hp.Float('dropout_1', 0.2, 0.5, step=0.1)))
    model.add(LSTM(units=hp.Int('units_2', min_value=50, max_value=200, step=50), 
                   return_sequences=False))
    model.add(Dropout(hp.Float('dropout_2', 0.2, 0.5, step=0.1)))
    model.add(Dense(units=hp.Int('dense_units', min_value=25, max_value=100, step=25)))
    model.add(Dense(1))  # Output layer for predicting the next close price

    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Initialize the tuner
tuner = kt.RandomSearch(build_model,
                        objective='val_loss',
                        max_trials=5,  # Increase trials for better search
                        executions_per_trial=10,
                        directory='tuning',
                        project_name='eth_lstm_with_indicators')

# Set early stopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=3)

# Perform the search
tuner.search(X, Y, epochs=15, validation_split=0.2, callbacks=[early_stopping])
best_model = tuner.get_best_models(num_models=1)[0]
best_model.summary()

# Save the best model
best_model.save('eth_lstm_best_strong_model_with_indicators.h5')
print("Hyperparameter tuning complete and best model saved.")
