import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Fetch historical Nvidia stock data from Yahoo Finance
nvidia_data = yf.download('NVDA', start='2017-01-01', end='2022-12-31')

# Display the first few rows of the downloaded data for verification
print(nvidia_data.head())

# Calculate the 50-day and 200-day moving averages
nvidia_data['MA50'] = nvidia_data['Close'].rolling(window=50).mean()
nvidia_data['MA200'] = nvidia_data['Close'].rolling(window=200).mean()

# Calculate Relative Strength Index (RSI) using a 14-day window
delta = nvidia_data['Close'].diff()  # Calculate the daily change in closing prices
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()  # Average gain over 14 days
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()  # Average loss over 14 days
rs = gain / loss  # Relative strength (RS)
nvidia_data['RSI'] = 100 - (100 / (1 + rs))  # Convert RS to RSI

# Calculate Moving Average Convergence Divergence (MACD)
nvidia_data['12_EMA'] = nvidia_data['Close'].ewm(span=12, adjust=False).mean()  # 12-day EMA
nvidia_data['26_EMA'] = nvidia_data['Close'].ewm(span=26, adjust=False).mean()  # 26-day EMA
nvidia_data['MACD'] = nvidia_data['12_EMA'] - nvidia_data['26_EMA']  # MACD line

# Display the last few rows of the data to confirm calculations
print(nvidia_data.tail())

# Drop rows with missing values to prepare data for modeling
nvidia_data.dropna(inplace=True)

# Define features (X) and target variable (y)
X = nvidia_data[['MA50', 'MA200', 'RSI', 'MACD']]  # Feature variables
y = nvidia_data['Close']  # Target variable (closing price)

# Split the data into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Display the shapes of the training and testing sets for confirmation
print(X_train.shape, X_test.shape)

# Create and train the Random Forest Regressor model
rf_model = RandomForestRegressor(n_estimators=500, max_depth=10, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = rf_model.predict(X_test)

# Evaluate model performance using MAE, MSE, and R-squared
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print the evaluation metrics
print(f'Mean Absolute Error: {mae}')
print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# Visualize actual vs. predicted stock prices
plt.figure(figsize=(12,6))
plt.plot(y_test.index, y_test, label='Actual Prices', color='blue')  # Plot actual prices
plt.plot(y_test.index, y_pred, label='Predicted Prices', color='red', linestyle='--')  # Plot predicted prices
plt.title('Nvidia Stock Price Prediction')  # Add title to the plot
plt.xlabel('Date')  # Label x-axis
plt.ylabel('Stock Price')  # Label y-axis
plt.legend()  # Add a legend to distinguish actual and predicted prices
plt.show()  # Display the plot


