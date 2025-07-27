# Mapping of full market names (including exchange) to yahooquery tickers by category

currency_futures = {
    "AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE": "AUDUSD=X",
    "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE": "GBPUSD=X",
    "CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE": "USDCAD=X",
    "EURO FX - CHICAGO MERCANTILE EXCHANGE": "EURUSD=X",
    "EURO FX/BRITISH POUND XRATE - CHICAGO MERCANTILE EXCHANGE": "EURGBP=X",
    "JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE": "JPY=X",
    "SWISS FRANC - CHICAGO MERCANTILE EXCHANGE": "CHF=X"
}

crypto_futures = {
    "BITCOIN - CHICAGO MERCANTILE EXCHANGE": "BTC-USD",  # spot proxy
    "MICRO BITCOIN - CHICAGO MERCANTILE EXCHANGE": "BTC-USD",  # no direct micro ticker on yahoo
    "MICRO ETHER - CHICAGO MERCANTILE EXCHANGE": "ETH-USD"    # no direct micro ticker on yahoo
}

equity_index_futures = {
    "E-MINI S&P FINANCIAL INDEX - CHICAGO MERCANTILE EXCHANGE": "ES=F",  # CME E-mini S&P 500 futures
    "DOW JONES U.S. REAL ESTATE IDX - CHICAGO BOARD OF TRADE": "DJR"  # ETF proxy for real estate index
}

energy_metals_futures = {
    "WTI CRUDE OIL FINANCIAL - NEW YORK MERCANTILE EXCHANGE": "CL=F",
    "PLATINUM - NEW YORK MERCANTILE EXCHANGE": "PL=F",
    "PALLADIUM - NEW YORK MERCANTILE EXCHANGE": "PA=F",
    "SILVER - COMMODITY EXCHANGE INC.": "SI=F",
    "COPPER - COMMODITY EXCHANGE INC.": "HG=F"
}

# Combine all mappings into a single dictionary
market_to_ticker = {
    **currency_futures,
    **crypto_futures,
    **equity_index_futures,
    **energy_metals_futures
}

# Function to get ticker by full market name
def get_yahooquery_ticker(market_name: str) -> str:
    return market_to_ticker.get(market_name.upper(), "Ticker Not Found")

# Test example
if __name__ == "__main__":
    test_markets = [
        "BITCOIN - CHICAGO MERCANTILE EXCHANGE",
        "EURO FX - CHICAGO MERCANTILE EXCHANGE",
        "WTI CRUDE OIL FINANCIAL - NEW YORK MERCANTILE EXCHANGE",
        "DOW JONES U.S. REAL ESTATE IDX - CHICAGO BOARD OF TRADE",
        "MICRO BITCOIN - CHICAGO MERCANTILE EXCHANGE",
        "AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE"
    ]
    for market in test_markets:
        ticker = get_yahooquery_ticker(market)
        print(f"{market}: {ticker}")
