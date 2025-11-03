"""
Predictions and Anomaly Detection Script

Purpose: Forecast future landing volumes using Prophet and detect anomalies using Isolation Forest.
Inputs: cleaned_data.csv
Outputs: Forecast plots, anomaly detection results saved in docs/
"""

import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# Load cleaned data
df = pd.read_csv('data/cleaned_data.csv')
df['date'] = pd.to_datetime(df['date'])
daily_landings = df.groupby('date')['landings'].sum().reset_index()

# Prepare data for Prophet
prophet_df = daily_landings.rename(columns={'date': 'ds', 'landings': 'y'})

# Fit Prophet model
model = Prophet()
model.fit(prophet_df)

# Make future dataframe for next 30 days
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Plot forecast
fig = model.plot(forecast)
plt.title('Landing Volume Forecast')
plt.savefig('docs/forecast.png')
plt.show()

# Anomaly detection using Isolation Forest
iso_forest = IsolationForest(contamination=0.1)  # Assume 10% anomalies
daily_landings['anomaly'] = iso_forest.fit_predict(daily_landings[['landings']])

# Plot anomalies
plt.figure(figsize=(10, 6))
plt.plot(daily_landings['date'], daily_landings['landings'], label='Landings')
anomalies = daily_landings[daily_landings['anomaly'] == -1]
plt.scatter(anomalies['date'], anomalies['landings'], color='red', label='Anomalies')
plt.title('Anomaly Detection in Landings')
plt.xlabel('Date')
plt.ylabel('Landings')
plt.legend()
plt.savefig('docs/anomalies.png')
plt.show()

print("Predictions and anomaly detection complete. Results saved in docs/")