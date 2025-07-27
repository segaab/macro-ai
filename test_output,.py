import pandas as pd
from data_fetch import fetch_data

# Fetch full data (last 5 years)
df = fetch_data()

# Convert Date column to datetime if it's not already
df['Date'] = pd.to_datetime(df['Date'])

# Filter to last 2 years
two_years_df = df[df['Date'] >= df['Date'].max() - pd.DateOffset(years=2)]

# Save to CSV
two_years_df.to_csv("macro_last_2_years.csv", index=False)

print("✅ Exported last 2 years of macro data to macro_last_2_years.csv")
