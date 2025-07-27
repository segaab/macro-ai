# app.py

import streamlit as st
import pandas as pd
from data_fetch import fetch_data
from phase_logic import identify_phase
from insights import generate_insights

# App title
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

# AI Insights
st.subheader("🤖 AI Insights on Current Macro Conditions")
ai_insights = generate_insights(two_years_df, macro_phase)
st.write(ai_insights)

# Download button
csv = two_years_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download 2-Year Data as CSV",
    data=csv,
    file_name='macro_last_2_years.csv',
    mime='text/csv',
)
