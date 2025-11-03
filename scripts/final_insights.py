"""
Final Insights and Reporting Script

Purpose: Compile final insights, generate summary plots, and prepare report-ready outputs.
Inputs: cleaned_data.csv, results from previous scripts
Outputs: Summary report in docs/final_report.md, additional plots
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv('data/cleaned_data.csv')
df['date'] = pd.to_datetime(df['date'])

# Key insights
total_landings = df['landings'].sum()
avg_daily_landings = df.groupby('date')['landings'].sum().mean()
peak_day = df.groupby('date')['landings'].sum().idxmax()

print(f"Total landings: {total_landings}")
print(f"Average daily landings: {avg_daily_landings}")
print(f"Peak landing day: {peak_day}")

# Final plot: Monthly landings
df['month'] = df['date'].dt.to_period('M')
monthly_landings = df.groupby('month')['landings'].sum()
plt.figure(figsize=(10, 6))
monthly_landings.plot(kind='bar')
plt.title('Monthly Landings')
plt.xlabel('Month')
plt.ylabel('Landings')
plt.savefig('docs/monthly_landings.png')
plt.show()

# Generate report
report = f"""
# Final Report: Aircraft Landing Patterns Analysis

## Summary
- Total landings: {total_landings}
- Average daily landings: {avg_daily_landings:.2f}
- Peak day: {peak_day}

## Key Findings
- Trends show [describe based on analysis]
- Anomalies detected [number]
- Forecast predicts [summary]

## Recommendations
- [Based on insights]
"""

with open('docs/final_report.md', 'w') as f:
    f.write(report)

print("Final insights generated. Report saved in docs/final_report.md")