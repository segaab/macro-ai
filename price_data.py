import pandas as pd
from yahooquery import Ticker
from datetime import datetime

def fetch_price_data(tickers, start_date, interval="1wk"):
    """Fetch weekly historical price data for a list of tickers"""
    df_all = []

    for symbol in tickers:
        try:
            ticker_obj = Ticker(symbol)
            hist = ticker_obj.history(start=start_date.strftime("%Y-%m-%d"), interval=interval)

            if isinstance(hist, pd.DataFrame) and not hist.empty:
                if 'date' in hist.columns:
                    hist.rename(columns={'date': 'Date'}, inplace=True)
                elif 'timestamp' in hist.columns:
                    hist.rename(columns={'timestamp': 'Date'}, inplace=True)
                else:
                    continue

                hist = hist.reset_index() if 'symbol' in hist.index.names else hist
                hist["Symbol"] = symbol
                hist["Return"] = hist["close"].pct_change()
                hist["Volatility"] = hist["Return"].rolling(4).std()  # 4-week rolling vol
                df_all.append(hist[["Date", "close", "Return", "Volatility", "Symbol"]])
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            continue

    if df_all:
        return pd.concat(df_all, ignore_index=True)
    else:
        return pd.DataFrame()
