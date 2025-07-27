# phase_logic.py

def identify_phase(df):
    df = df.sort_values('Date')
    latest = df.iloc[-1]
    fedrate_latest = latest['FedRate']
    yield_latest = latest['10Y_Yield']
    
    fedrate_6m_ago = df.iloc[-7]['FedRate']
    fedrate_12m_ago = df.iloc[-13]['FedRate']
    
    rate_cut_6m = fedrate_6m_ago - fedrate_latest
    rate_cut_12m = fedrate_12m_ago - fedrate_latest
    rate_stable = abs(fedrate_6m_ago - fedrate_latest) < 0.25
    
    if rate_cut_12m >= 1.0 and fedrate_latest < yield_latest:
        return "Early Recovery"
    elif rate_stable and yield_latest - fedrate_latest >= 0.75:
        return "Mid Expansion"
    elif fedrate_latest >= 4.5 and (yield_latest - fedrate_latest <= 0.25):
        return "Late Cycle"
    elif rate_cut_6m >= 1.0 and yield_latest < fedrate_latest:
        return "Recession"
    else:
        return "Transition"
