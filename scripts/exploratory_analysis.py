"""
Exploratory Data Analysis Script

Purpose: Perform exploratory data analysis on the cleaned dataset, including summary statistics and visualizations.
Inputs: cleaned_data.csv
Outputs: Summary statistics printed, plots saved in docs/ folder
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv('data/cleaned_data.csv')
df['date'] = pd.to_datetime(df['date'])  # Ensure date is datetime

# Summary statistics
print("Summary statistics:")
print(df.describe())

# Check for correlations
# Assuming numerical columns; adjust as needed
numerical_cols = df.select_dtypes(include=[np.number]).columns
correlation_matrix = df[numerical_cols].corr()
print("\nCorrelation matrix:")
print(correlation_matrix)

# Visualize landings over time
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['landings'])  # Placeholder
plt.title('Aircraft Landings Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Landings')
plt.savefig('docs/landings_over_time.png')
plt.show()

# Distribution of landings
plt.figure(figsize=(8, 5))
sns.histplot(df['landings'], bins=30)
plt.title('Distribution of Landings')
plt.savefig('docs/landings_distribution.png')
plt.show()

# If there are categorical columns, e.g., aircraft_type
if 'aircraft_type' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='aircraft_type')
    plt.title('Count of Aircraft Types')
    plt.xticks(rotation=45)
    plt.savefig('docs/aircraft_types.png')
    plt.show()

print("Exploratory analysis complete. Plots saved in docs/")