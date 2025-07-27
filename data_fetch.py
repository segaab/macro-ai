import pandas as pd
from fredapi import Fred
from datetime import datetime, timedelta
import os

def fetch_data():
    # --- Define date range: last 5 years ---
    end_date = datetime.today()
    start_date = end_date - timedelta(days=5*365)

    # --- Initialize FRED client ---
    fred = Fred(api_key="91bb2c5920fb8f843abdbbfdfcab5345")

    # --- Get Fed Funds Rate ---
    fed_rate_series = fred.get_series('FEDFUNDS', start_date, end_date)
    fed_rate_df = fed_rate_series.reset_index()
    fed_rate_df.columns = ['Date', 'FedRate']
    fed_rate_df['Date'] = pd.to_datetime(fed_rate_df['Date'])

    # --- Get 10Y Treasury Yield (constant maturity) ---
    yield_series = fred.get_series('GS10', start_date, end_date)
    yield_df = yield_series.reset_index()
    yield_df.columns = ['Date', '10Y_Yield']
    yield_df['Date'] = pd.to_datetime(yield_df['Date'])

    # --- Merge on Date with outer join to keep all dates ---
    merged_df = pd.merge(fed_rate_df, yield_df, how='outer', on='Date')

    # --- Sort by Date ---
    merged_df = merged_df.sort_values('Date').reset_index(drop=True)

    return merged_df
