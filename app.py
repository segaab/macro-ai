# app.py

import streamlit as st
import pandas as pd
from data_fetch import fetch_data
from phase_logic import identify_phase
from insights import generate_macro_insight, generate_insights, parse_speculation_output, evaluate_speculation_playout

# NOTE: Import or define this function for speculation progress analysis
# from some_module import analyze_speculation_progress


st.set_page_config(layout="wide")
st.title("🧭 Macro Phase Identifier Dashboard")

# Load data
data_load_state = st.text("📦 Fetching macroeconomic data...")
df = fetch_data()
data_load_state.text("✅ Data fetched successfully!")

# Filter last 2 years
two_years_df = df[df['Date'] >= pd.to_datetime(df['Date'].max()) - pd.DateOffset(years=2)]

# Show raw data
if st.checkbox("📄 Show raw data (last 2 years)"):
    st.dataframe(two_years_df)

# Identify phase and profile
st.subheader("📊 Macro Phase Assessment")
macro_phase = identify_phase(two_years_df)
st.write(f"🧠 Inferred Macro Phase: **{macro_phase}**")

if 'insights_text' not in st.session_state:
    st.session_state.insights_text = None

# Generate AI insights button
if st.button("💡 Generate AI Insights"):
    insights_text = generate_insights(two_years_df, macro_phase)
    st.session_state.insights_text = insights_text.text.strip()

# Show AI insights if available
if st.session_state.insights_text:
    st.subheader("🤖 AI Insights on Current Macro Conditions")
    st.write(st.session_state.insights_text)

    st.markdown("----")
    st.subheader("🔍 Monitor Suggested Speculative Plays")

    # Show the speculative trades tracking button
    if st.button("📈 Track Speculative Trades"):
        # Parse output once here
        parsed_info = generate_macro_insight(two_years_df, macro_phase)
        print('Logs:', parsed_info)
        # Extract separate lists
        def remove_asterisk_dash(text):
            return text.replace("- ****", "").strip()
        tickers = [s["Ticker"] for s in parsed_info if s["Ticker"]]
        ticker = remove_asterisk_dash(str(tickers))
        cot_names = [s["COT Name"] for s in parsed_info if s["COT Name"]]
        cot_name = remove_asterisk_dash(str(cot_names))
        speculation = [s["Speculation"] for s in parsed_info if s["Speculation"]]
        #suggestions = ', '.join(str(item) for item in parsed_info)

        # Check if analyze_speculation_progress function exists
        if 'evaluate_speculation_playout' in globals():
            tracking_result = evaluate_speculation_playout(speculation, tickers, cot_names)
            st.subheader("📊 Speculation Monitoring Result")
            st.write(tracking_result)
        else:
            st.warning("⚠️ Function 'analyze_speculation_progress' is not implemented or imported.")

# Download button
csv = two_years_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download 2-Year Data as CSV",
    data=csv,
    file_name='macro_last_2_years.csv',
    mime='text/csv',
)
