import requests
import pandas as pd
from datetime import datetime

def fetch_oecd_interest_rates_new(country_code, indicator="IR3TIB", frequency="A", start_year=2023, end_year=2025):
    """
    Fetch interest rates from OECD's new SDMX-JSON API (v1).
    
    Parameters:
        country_code (str): OECD country code (e.g., EA19 for Euro Area)
        indicator (str): Indicator code, default IR3TIB (3-month interest rate)
        frequency (str): Frequency, e.g. 'A' (annual), 'M' (monthly)
        start_year (int): start year
        end_year (int): end year

    Returns:
        pd.DataFrame: DataFrame with date and interest rate
    """
    # Build filter expression for the new API format:
    # According to doc, filter expression is:
    # <dimension1>.<dimension2>.<frequency>
    # For example: EA19.IR3TIB.A
    filter_expr = f"{country_code}.{indicator}.{frequency}"
    
    # Construct URL with new RESTful v1 syntax (comma separated identifiers):
    url = (
        f"https://sdmx.oecd.org/public/rest/data/OECD,IR3TIB,1.0/"
        f"{filter_expr}/?format=jsondata"
        f"&startPeriod={start_year}&endPeriod={end_year}"
        f"&dimensionAtObservation=AllDimensions"
    )
    
    print(f"Fetching from OECD SDMX API: {url}")
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    # Parse SDMX-JSON structure to extract observations
    # The observations are nested inside data -> dataSets -> series
    series = data["data"]["dataSets"][0]["series"]
    structure = data["data"]["structure"]
    
    # Get time periods from the structure
    time_values = structure["dimensions"]["observation"][0]["values"]
    dates = [tv["id"] for tv in time_values]  # e.g., ['2023', '2024', '2025']

    records = []
    for series_key, series_value in series.items():
        obs = series_value.get("observations", {})
        for obs_idx_str, obs_val in obs.items():
            obs_idx = int(obs_idx_str)
            date = dates[obs_idx]
            value = obs_val[0]  # first value in the list is the data value
            # Append record as (date, value)
            records.append({"date": pd.to_datetime(date), "interest_rate": value})
    
    df = pd.DataFrame(records).sort_values("date").reset_index(drop=True)
    return df


def fetch_us_interest_rates_fred(start_date="2023-01-01", end_date="2025-07-27"):
    from fredapi import Fred
    fred = Fred(api_key="91bb2c5920fb8f843abdbbfdfcab5345")
    series = fred.get_series('FEDFUNDS', observation_start=start_date, observation_end=end_date)
    df = series.reset_index()
    df.columns = ["date", "interest_rate"]
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date").sort_index()
    return df


def test_fetch_and_save():
    test_cases = [
        ("United States", None),  # Uses FRED
        ("European Union", "EA19"),
        ("Japan", "JPN"),
        ("Canada", "CAN"),
    ]
    
    for country_name, code in test_cases:
        print(f"\nFetching interest rates for: {country_name}")
        try:
            if country_name == "United States":
                df = fetch_us_interest_rates_fred()
            else:
                df = fetch_oecd_interest_rates_new(code)
            print(df.head())
            filename = f"{country_name.replace(' ', '_')}_interest_rates.csv"
            df.to_csv(filename, index=False)
            print(f"Saved to {filename}")
        except Exception as e:
            print(f"Error fetching data for {country_name}: {e}")

if __name__ == "__main__":
    test_fetch_and_save()
