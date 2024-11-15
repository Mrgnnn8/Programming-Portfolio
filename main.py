import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Download Nvidia stock data (NVDA) for the past 5 years
nvidia_data = yf.download('NVDA', start='2017-01-01', end='2022-12-31')

# Display the first few rows of the dataset
print(nvidia_data.head())

# Calculate 50-day and 200-day moving averages
nvidia_data['MA50'] = nvidia_data['Close'].rolling(window=50).mean()
nvidia_data['MA200'] = nvidia_data['Close'].rolling(window=200).mean()

# Calculate the RSI (Relative Strength Index)
delta = nvidia_data['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
nvidia_data['RSI'] = 100 - (100 / (1 + rs))

# Calculate MACD (Moving Average Convergence Divergence)
nvidia_data['12_EMA'] = nvidia_data['Close'].ewm(span=12, adjust=False).mean()
nvidia_data['26_EMA'] = nvidia_data['Close'].ewm(span=26, adjust=False).mean()
nvidia_data['MACD'] = nvidia_data['12_EMA'] - nvidia_data['26_EMA']

# Display the updated data
print(nvidia_data.tail())

# Drop rows with missing values
nvidia_data.dropna(inplace=True)

# Define features (X) and target (y)
X = nvidia_data[['MA50', 'MA200', 'RSI', 'MACD']]
y = nvidia_data['Close']  # We want to predict the closing price

# Split the data into training and testing sets (80% train, 20% test)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

print(X_train.shape, X_test.shape)

# Initialize and train the Random Forest model
rf_model = RandomForestRegressor(n_estimators=500, max_depth=10, random_state=42)
rf_model.fit(X_train, y_train)

# Predict on the test set
y_pred = rf_model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Absolute Error: {mae}')
print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# Plot the actual vs predicted stock prices
plt.figure(figsize=(12,6))
plt.plot(y_test.index, y_test, label='Actual Prices', color='blue')
plt.plot(y_test.index, y_pred, label='Predicted Prices', color='red', linestyle='--')
plt.title('Nvidia Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.show()

