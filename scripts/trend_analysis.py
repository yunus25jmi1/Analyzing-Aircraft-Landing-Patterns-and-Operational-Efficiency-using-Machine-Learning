"""
Trend Analysis Script

Purpose: Analyze trends in the landing data using statistical methods and machine learning.
Inputs: cleaned_data.csv
Outputs: Trend analysis results, plots saved in docs/
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib

# Load cleaned data
df = pd.read_csv('data/cleaned_data.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Aggregate by date if multiple entries per day
daily_landings = df.groupby('date')['landings'].sum().reset_index()

# Simple linear regression to model trend
daily_landings['days'] = (daily_landings['date'] - daily_landings['date'].min()).dt.days
X = daily_landings[['days']]
y = daily_landings['landings']

model = LinearRegression()
model.fit(X, y)
predictions = model.predict(X)

# Save the model
joblib.dump(model, 'models/trend_model.pkl')

# Plot trend
plt.figure(figsize=(10, 6))
plt.scatter(daily_landings['date'], y, label='Actual')
plt.plot(daily_landings['date'], predictions, color='red', label='Trend Line')
plt.title('Landing Trend Analysis')
plt.xlabel('Date')
plt.ylabel('Landings')
plt.legend()
plt.savefig('docs/trend_analysis.png')
plt.show()

# Calculate trend slope
slope = model.coef_[0]
print(f"Trend slope: {slope} landings per day")

# MSE
mse = mean_squared_error(y, predictions)
print(f"Mean Squared Error: {mse}")

# Seasonal decomposition if enough data
# Using statsmodels for decomposition
from statsmodels.tsa.seasonal import seasonal_decompose

if len(daily_landings) > 12:  # Assuming monthly data
    daily_landings.set_index('date', inplace=True)
    decomposition = seasonal_decompose(daily_landings['landings'], model='additive', period=12)
    decomposition.plot()
    plt.savefig('docs/seasonal_decomposition.png')
    plt.show()

print("Trend analysis complete.")