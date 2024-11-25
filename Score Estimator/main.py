import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('student_scores.csv')  # Read the CSV file into a Pandas DataFrame

# Define features (Hours studied) and target variable (Exam Score)
X = data[['Hours']]  # Features - Hours studied
y = data['Score']    # Target - Exam scores

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)  # Fit the model to the training data

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate Mean Absolute Error to evaluate model performance
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error: {mae:.2f}')  # Print the MAE to
