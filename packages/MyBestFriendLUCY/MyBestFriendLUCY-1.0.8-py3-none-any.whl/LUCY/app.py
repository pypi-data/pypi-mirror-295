import os
from pathlib import Path
import random
import ccxt
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import json

# Resolve base directory and model/scaler paths
base_dir = Path(__file__).resolve().parent
model_path = os.path.join(base_dir, 'eth_lstm_best_strong_greatest_model.h5')
scaler_path = os.path.join(base_dir, 'scaler_custom.pkl')
history_file = os.path.join(base_dir, 'trade_history.json')

# Load the model and scaler, ensuring they're actual objects and not strings
model = tf.keras.models.load_model(model_path)
scaler = joblib.load(scaler_path)

# Initialize Binance API
binance = ccxt.binance()

# Function to load trade history from JSON file
def load_trade_history():
    if not os.path.exists(history_file):
        return {"total": 0, "success": 0, "fail": 0}
    with open(history_file, 'r') as file:
        return json.load(file)

# Function to save trade history to JSON file
def save_trade_history(history):
    with open(history_file, 'w') as file:
        json.dump(history, file)

# Function to update trade history with success or failure
def update_trade_history(success):
    history = load_trade_history()
    history['total'] += 1
    if success:
        history['success'] += 1
    else:
        history['fail'] += 1
    save_trade_history(history)
    return history

# Function to calculate accuracy
def calculate_accuracy(history):
    if history['total'] == 0:
        return 0.0
    return (history['success'] / history['total']) * 100

# Function to show the accuracy
def show_accuracy():
    history = load_trade_history()
    accuracy = calculate_accuracy(history)
    print(f"Lucy: My current prediction accuracy is {accuracy:.2f}%.")

# Function to fetch the current price
def fetch_current_price(symbol):
    try:
        ticker = binance.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        print(f"Error fetching current price: {str(e)}")
        return None

# Function to fetch the latest 48 close prices in real-time (30-minute intervals)
def fetch_latest_data(symbol='ETH/USDT', timeframe='30m', limit=48):
    try:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
        return np.array([x[4] for x in ohlcv])  # Return the close prices
    except Exception as e:
        print(f"Error fetching latest data: {str(e)}")
        return None

# Function to format text with color
def color_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def make_prediction_and_suggest_stop_loss():
    symbol = 'ETH/USDT'
    
    # Fetch current price
    current_price = fetch_current_price(symbol)
    if current_price is None:
        print("Unable to fetch the current price. Exiting.")
        return None, None
    
    # Fetch the latest 48 data points
    latest_data = fetch_latest_data(symbol=symbol, timeframe='30m', limit=48)
    if latest_data is None or len(latest_data) < 48:
        print('Not enough data to make a prediction. Exiting.')
        return None, None
    
    # Preprocess the data
    latest_data = latest_data.reshape(-1, 1)
    latest_data_df = pd.DataFrame(latest_data, columns=['close'])
    latest_data_scaled = scaler.transform(latest_data_df)
    latest_data_scaled = latest_data_scaled.reshape(1, latest_data_scaled.shape[0], 1)
    
    # Make prediction
    prediction = model.predict(latest_data_scaled, verbose=0)
    predicted_price_1h_ahead = scaler.inverse_transform(prediction).flatten()[0]
    
    # Calculate the percentage change
    percentage_change = ((predicted_price_1h_ahead - current_price) / current_price) * 100

    # Format percentage change in green for positive and red for negative, regardless of magnitude
    if percentage_change >= 0:
        formatted_percentage = color_text(f"{round(percentage_change, 2)}%", 32)  # Green for positive change
    else:
        formatted_percentage = color_text(f"{round(percentage_change, 2)}%", 31)  # Red for negative change

    # Determine buy/sell suggestion with independent colors
    suggestion = ""
    if percentage_change > 1.5:
        suggestion = color_text("definite buy", 32)  # Green
    elif 1.0 <= percentage_change <= 1.5:
        suggestion = color_text("buy!", 32)  # Green
    elif 0.75 <= percentage_change < 1.0:
        suggestion = color_text("highly recommended buy", 32)  # Green
    elif 0.5 <= percentage_change < 0.75:
        suggestion = color_text("recommended buy", 32)  # Green
    elif 0.3 <= percentage_change < 0.5:
        suggestion = color_text("possible buy", 32)  # Green
    elif -0.5 <= percentage_change < -0.3:
        suggestion = color_text("possible sell", 33)  # Orange
    elif -0.75 <= percentage_change < -0.5:
        suggestion = color_text("recommended sell", 33)  # Orange
    elif -1.0 <= percentage_change < -0.75:
        suggestion = color_text("highly recommended sell", 33)  # Orange
    elif -1.5 <= percentage_change < -1.0:
        suggestion = color_text("sell!", 33)  # Orange
    elif percentage_change < -1.5:
        suggestion = color_text("definite sell", 33)  # Orange
    elif -0.29 <= percentage_change <= 0.29:
        suggestion = color_text("neutral position", 37)  # Grey for neutral change
    
    # Calculate stop loss
    if predicted_price_1h_ahead > current_price:
        stop_loss = current_price - abs(predicted_price_1h_ahead - current_price)
    else:
        stop_loss = current_price + abs(predicted_price_1h_ahead - current_price) 

    # Response with formatted output
    response = (
        f"Lucy: ETH is valued at \033[35m${round(current_price, 2)}\033[0m right now. "
        f"In one hour, my prediction says it will be \033[35m${round(predicted_price_1h_ahead, 2)}\033[0m, "
        f"showing a {formatted_percentage} shift. "
        f"I suggest a {suggestion} on this one. "
        f"You might consider a stop loss at ${round(stop_loss, 2)}."
    )

    print(response)
    
    # Return current and predicted price for further use
    return current_price, predicted_price_1h_ahead

# Function to update trade history based on user input
def update_history():
    
    # Ask the user if the prediction was correct or not
    result = input("Providing feedback can help me lots! But down to business, was the prediction successful? (just use yes or no)").strip().lower()
    if result == 'yes':
        update_trade_history(success=True)
        print("Lucy: I've marked that trade marked as successful. Thanks for that feedback!")
    elif result == 'no':
        update_trade_history(success=False)
        print("Lucy: I've marked that trade marked as failed. Thanks for the feedback!")
    else:
        print("Lucy: I don't understand 🤔")

def main():
    print("Hi there, I'm Lucy, your personal trade assistant. If you don't already know, you can learn how to talk to me by pressing i.")

    while True:
        user_input = input("\nYou: ").strip().lower()

        if 'predict' in user_input:
            make_prediction_and_suggest_stop_loss()
        elif any(keyword in user_input for keyword in ['accuracy', 'rate', '%', 'success rate', 'success']):
            show_accuracy()
        elif any(keyword in user_input for keyword in ['history', 'recent', 'trades', 'update', 'json']):
            update_history()
        elif user_input == 'exit':
            print("Lucy: Goodbye!")
            break
        elif user_input == 'i':
            print("Using the word 'predict' will make a prediction, Using the word 'accuracy' will show you the prediction accuracy, saying anything along the lines of 'update history' will update the trade results file, and say 'exit' to quit.")
        elif user_input == 'calculator':
            print("Lucy: Calculator mode activated.")
        elif user_input in ['thanks', 'thank you', 'thx']:
            responses = ["You're welcome!", "No problem!", "Glad to help!", "Anytime!", "Happy to assist!"]
            print(f"Lucy: {random.choice(responses)}")
        elif user_input in ['hello', 'yo', 'hi', 'hi lucy', 'hello lucy']:
            greetings = ["Hello!", "Hey there!", "Hi!", "Yo! What's up?"]
            print(f"Lucy: {random.choice(greetings)}")
        else:
            print("Lucy: I don't understand 🤷")

if __name__ == '__main__':
    main()