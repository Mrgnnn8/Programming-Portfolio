# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# Load the dataset
# The dataset contains 'Hours' studied and 'Score' achieved
data = pd.read_csv('student_scores.csv')

# Define the feature(s) and target variable
X = data[['Hours']]  # Feature: Hours studied
y = data['Score']    # Target: Exam Score

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model's performance using Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error: {mae:.2f}')

# Visualize the data points and the fitted regression line
plt.scatter(X, y, color='blue', label='Actual Scores')  # Scatter plot of actual data
plt.plot(X, model.predict(X), color='red', label='Regression Line')  # Regression line
plt.xlabel('Hours Studied')
plt.ylabel('Exam Score')
plt.title('Hours Studied vs Exam Score')
plt.legend()
plt.show()

