"""
Data Loading and Initial Cleaning Script

Purpose: Load the Air Traffic Landings dataset from Kaggle and perform initial data cleaning.
Inputs: air_traffic_landings.csv in data/ folder
Outputs: Cleaned pandas DataFrame saved as cleaned_data.csv
"""

import pandas as pd
import numpy as np

# Load the dataset
# Replace 'air_traffic_landings.csv' with the actual filename if different
df = pd.read_csv('data/air-traffic-landings-statistics.csv')

# Inspect the first few rows to understand the structure
print("First 5 rows of the dataset:")
print(df.head())

# Inspect column names and data types
print("\nColumn names and data types:")
print(df.dtypes)

# Handle missing values - for example, drop rows with missing critical data
# Assuming 'Activity Period' and 'Landing Count' are critical; adjust based on actual columns
df.dropna(subset=['Activity Period', 'Landing Count'], inplace=True)  # Placeholder columns

# Convert Activity Period to datetime (format YYYYMM)
df['Activity Period'] = pd.to_datetime(df['Activity Period'], format='%Y%m')

# Rename columns for ease
df.rename(columns={'Activity Period': 'date', 'Landing Count': 'landings'}, inplace=True)

# Remove duplicates if any
df.drop_duplicates(inplace=True)

# Basic data validation - e.g., ensure landings are positive
df = df[df['landings'] > 0]  # Placeholder

# Save cleaned data
df.to_csv('data/cleaned_data.csv', index=False)

print("Data loaded and cleaned. Cleaned data saved to data/cleaned_data.csv")