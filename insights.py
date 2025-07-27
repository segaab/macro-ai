import os
import google.generativeai as genai
import pandas as pd

# Configure Gemini API
genai.configure(api_key="AIzaSyCLsb1T1JPzcmfc3zP6dALRAnH0sB22lvM")

MODEL_NAME = "models/gemini-2.5-flash"

def generate_insights(df: pd.DataFrame, macro_phase: str) -> str:
    """
    Generates AI insights using the last 2 years of data, the current macro profile, and macro phase label.

    Parameters:
        df (pd.DataFrame): DataFrame with historical macroeconomic data.
        macro_profile (str): Textual description of the current macroeconomic profile.
        macro_phase (str): Current macro phase classification (e.g., Expansion, Recession).
    
    Returns:
        str: Insightful analysis from Gemini.
    """
    # Ensure datetime format and filter last 2 years
    df['Date'] = pd.to_datetime(df['Date'])
    last_2_years_df = df[df['Date'] >= df['Date'].max() - pd.DateOffset(years=2)]

    prompt = f"""
You are a hedge fund macroeconomy analyst.

--- Current Macro Phase ---
{macro_phase}

--- Historical Macroeconomic Data (Last 2 Years) ---
{last_2_years_df.to_string(index=False)}

Tasks:
1. Evaluate whether the given macro phase ("{macro_phase}") is accurate based on the data and profile.
2. Highlight any inconsistencies or indicators suggesting a different phase.
3. Identify early warning signs or opportunities.
4. Forecast macroeconomic trends for the next 3–6 months.
5. Suggest one speculative move, if applicable

Be precise and explain your reasoning.
"""

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error generating insights: {str(e)}"
