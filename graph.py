import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the datasets
with_ai = pd.read_csv('with_ai_productivity.csv', names=['Date', 'Activity', 'Time', 'Status'])
without_ai = pd.read_csv('without_ai_productivity.csv', names=['Date', 'Activity', 'Time', 'Status'])

# Calculate activity counts
with_ai_activity_counts = with_ai['Activity'].value_counts()
without_ai_activity_counts = without_ai['Activity'].value_counts()

# Get a unified list of activities
activities = set(with_ai_activity_counts.index).union(set(without_ai_activity_counts.index))
activities = sorted(activities)

# Prepare counts for both datasets
with_ai_counts = [with_ai_activity_counts.get(activity, 0) for activity in activities]
without_ai_counts = [without_ai_activity_counts.get(activity, 0) for activity in activities]

# Plot comparison of activity counts
x = np.arange(len(activities))
width = 0.35

plt.figure(figsize=(12, 6))
plt.bar(x - width/2, with_ai_counts, width, label='With AI')
plt.bar(x + width/2, without_ai_counts, width, label='Without AI')
plt.xticks(x, activities, rotation=45, ha='right')
plt.title('Comparison of Activity Counts')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.show()

