import pandas as pd
from sodapy import Socrata
import os

# Load credentials from environment variables
MY_APP_TOKEN = os.getenv("WSCaavlIcDgtLVZbJA1FKkq40")
USERNAME = os.getenv("segaw120@gmail.com")
PASSWORD = os.getenv("SwingFirst@135")

# Initialize Socrata client
client = Socrata("publicreporting.cftc.gov",
                 MY_APP_TOKEN,
                 username=USERNAME,
                 password=PASSWORD)

# Dataset ID for COT
COT_DATASET_ID = "6dca-aqww"


group_list = {'BASE METAL','CRYPTOCURRENCIES', 'CURRENCY', 'NATURAL GAS AND PRODUCTS', 'PRECIOUS METALs', 'STOCK INDICIES'}
def get_latest_cot_markets():
    # Step 1: Get latest report date
    latest_date_result = client.get(COT_DATASET_ID,
                                    select="report_date_as_yyyy_mm_dd",
                                    order="report_date_as_yyyy_mm_dd DESC",
                                    limit=1)

    if not latest_date_result:
        print("❌ Failed to retrieve latest report date.")
        return pd.DataFrame()

    latest_date = latest_date_result[0]['report_date_as_yyyy_mm_dd']
    print(f"📅 Latest COT Report Date: {latest_date}")

    # Step 2: Compose correct where clause using IN
    where_clause = (
        f"report_date_as_yyyy_mm_dd = '{latest_date}' AND "
        f"commodity_subgroup_name IN ('BASE METAL', 'CRYPTOCURRENCIES', 'CURRENCY', 'NATURAL GAS AND PRODUCTS', 'PRECIOUS METALs', 'STOCK INDICIES')"
    )

    # Step 3: Get all records from the latest report date filtered by subgroup names
    result = client.get(COT_DATASET_ID,
                        where=where_clause,
                        select="market_and_exchange_names")

    df = pd.DataFrame.from_records(result).drop_duplicates().sort_values(by='market_and_exchange_names')
    df.to_csv("cot_latest_market_names.csv", index=False)
    print("✅ Exported market names to 'cot_latest_market_names.csv'")
    print(len(df))
    return df


if __name__ == "__main__":
    get_latest_cot_markets()
