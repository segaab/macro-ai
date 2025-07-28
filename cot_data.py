import pandas as pd
from datetime import datetime, timedelta
from sodapy import Socrata

# Initialize Socrata client using environment variables
client = Socrata(
    "publicreporting.cftc.gov",
    "WSCaavlIcDgtLVZbJA1FKkq40"
)

def fetch_cot_for_tickers(cot_names, start_date):
    """Fetch 6 months of COT data for given market_and_exchange_names"""
    df_all = []

    # Format start_date to match dataset
    start_str = start_date.strftime("%Y-%m-%d")

    for name in cot_names:
        results = client.get(
            "6dca-aqww",
            where=f"report_date_as_yyyy_mm_dd >= '{start_str}' AND market_and_exchange_names = '{name}'",
            limit=10000
        )
        if results:
            df = pd.DataFrame.from_records(results)
            df["market_and_exchange_names"] = name
            df_all.append(df)

    if df_all:
        combined = pd.concat(df_all, ignore_index=True)
        combined["report_date_as_yyyy_mm_dd"] = pd.to_datetime(combined["report_date_as_yyyy_mm_dd"])
        return combined.sort_values("report_date_as_yyyy_mm_dd")
    else:
        return pd.DataFrame()
