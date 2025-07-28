import os
import google.generativeai as genai
import pandas as pd
from market_object import market_to_ticker
from datetime import datetime, timedelta
from cot_data import fetch_cot_for_tickers
from price_data import fetch_price_data

# Configure Gemini API
genai.configure(api_key="AIzaSyCLsb1T1JPzcmfc3zP6dALRAnH0sB22lvM")

MODEL_NAME = "models/gemini-2.5-pro"

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
    5. Suggest one speculative move, if applicable, with a list of futures tickers. Choose from the following list: {market_to_ticker}. 

    Return speculation suggestion in the following format:
       - Speculation: <idea>
       - Ticker: <futures ticker symbol> 
       - COT Name: <COT official name>
       - Reasoning: <macro rationale>

    Be precise and explain your reasoning.
    """

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        result = model.generate_content(prompt)

        return result 
    except Exception as e:
        return f"❌ Error generating insights: {str(e)}"

import re

def parse_speculation_output(text):
    """
    Parses speculation suggestions from the AI response.
    Returns a list of dictionaries with Speculation, Ticker, COT Name, and Reasoning.
    Handles multiline reasoning and variable spacing.
    """
    print('Logs:',str(text))
    suggestions = []
    blocks = text.split("- Speculation:")

    for block in blocks[1:]:  # Skip anything before the first Speculation block
        lines = block.strip().splitlines()
        current = {"Speculation": "", "Ticker": "", "COT Name": "", "Reasoning": ""}
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("Ticker:"): #or line.startswith("*   **Ticker:**") or line.startswith("- **Ticker:**"):
                current["Speculation"] = "\n".join(lines[:i]).strip()
                current["Ticker"] = line.replace("Ticker:", "").strip()
            elif line.startswith("*   **Ticker:**"): #or line.startswith("*   **Ticker:**") or line.startswith("- **Ticker:**"):
                current["Speculation"] = "\n".join(lines[:i]).strip()
                current["Ticker"] = line.replace("Ticker:", "").strip()
            elif line.startswith("- **Ticker:**"): #or line.startswith("*   **Ticker:**") or line.startswith("- **Ticker:**"):
                current["Speculation"] = "\n".join(lines[:i]).strip()
                current["Ticker"] = line.replace("Ticker:", "").strip()
            elif line.startswith("- **Ticker**:"): #or line.startswith("*   **Ticker:**") or line.startswith("- **Ticker:**"):
                current["Speculation"] = "\n".join(lines[:i]).strip()
                current["Ticker"] = line.replace("Ticker:", "").strip()
            elif line.startswith("COT Name:"): # or line.startswith("*   **COT Name:**") or line.startswith("- **COT Name:**"):
                current["COT Name"] = line.replace("COT Name:", "").strip()
            elif line.startswith("- **COT Name**:"): # or line.startswith("*   **COT Name:**") or line.startswith("- **COT Name:**"):
                current["COT Name"] = line.replace("COT Name:", "").strip()
            elif line.startswith("*   **COT Name:**"): # or line.startswith("*   **COT Name:**") or line.startswith("- **COT Name:**"):
                current["COT Name"] = line.replace("COT Name:", "").strip()
            elif line.startswith("- **COT Name:**"): # or line.startswith("*   **COT Name:**") or line.startswith("- **COT Name:**"):
                current["COT Name"] = line.replace("COT Name:", "").strip()
            elif line.startswith("Reasoning:"): # or line.starstwith("*   **Reasoning:**") or line.starstwith("- **Reasoning:**"):
                reasoning_lines = [line.replace("Reasoning:", "").strip()]
            elif line.startswith("- **Reasoning**:"): # or line.starstwith("*   **Reasoning:**") or line.starstwith("- **Reasoning:**"):
                reasoning_lines = [line.replace("Reasoning:", "").strip()]
            elif line.startswith("*   **Reasoning:**"): # or line.starstwith("*   **Reasoning:**") or line.starstwith("- **Reasoning:**"):
                reasoning_lines = [line.replace("Reasoning:", "").strip()]
            elif line.startswith("- **Reasoning:**"): # or line.starstwith("*   **Reasoning:**") or line.starstwith("- **Reasoning:**"):
                reasoning_lines = [line.replace("Reasoning:", "").strip()]
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("Speculation:"):
                    reasoning_lines.append(lines[i].strip())
                    i += 1
                current["Reasoning"] = " ".join(reasoning_lines).strip()
                break  # Done with this block
            i += 1
        suggestions.append(current)

    return suggestions




def evaluate_speculation_playout(speculation, tickers, cot_names):
    print('Logs:',str(speculation), str(tickers), str(cot_names))
    # Step 1: Define date range
    six_months_ago = datetime.today() - timedelta(weeks=26)

    # Step 3: Fetch COT and price data
    cot_data = fetch_cot_for_tickers(cot_names, six_months_ago)
    price_data = fetch_price_data(tickers, six_months_ago, interval="1wk")

    # Step 4: Format data for feedback to model
    cot_data_snapshot = cot_data.head(10).to_string() if not cot_data.empty else "No COT data found."
    price_data_snapshot = price_data.head(10).to_string() if not price_data.empty else "No price data found."

    analysis_prompt = f"""
    The following are speculative macro plays previously suggested.
    You are given 6 months of positioning data and price returns/volatility.
    Assess whether the speculation is playing out or if trends are reversing.

    Speculation:
    {speculation}

    COT Data Snapshot:
    {cot_data_snapshot}

    Price Data Snapshot:
    {price_data_snapshot}

    Provide updated commentary for each speculation.
    """
    model = genai.GenerativeModel(MODEL_NAME)
    final_analysis = model.generate_content(analysis_prompt)
    return final_analysis.text.strip()

def generate_macro_insight(df: pd.DataFrame, macro_phase: str):
    print('Logs:',str(macro_phase))
    try:
        # Get full structured response from Gemini
        response = generate_insights(df, macro_phase)
        # Extract actual text from deeply nested Gemini response
        content = response.candidates[0].content.parts[0].text.strip()
        print('Content Logs:',str(content))
        # Split the insight and speculative section (optional step)
        if "**5. Speculative Move:**" in content:
            macro_analysis, speculation_part = content.split("**5. Speculative Move:**", 1)
            speculation_text = f"- Speculation:{speculation_part.strip()}"
        elif "### 5. Speculative Move" in content:
            macro_analysis, speculation_part = content.split("### 5. Speculative Move", 1)
            speculation_text = f"- Speculation:{speculation_part.strip()}"
        elif "### **5. Speculative Move**" in content:
            macro_analysis, speculation_part = content.split("### **5. Speculative Move**", 1)
            speculation_text = f"- Speculation:{speculation_part.strip()}"
        else:
            macro_analysis = content
            speculation_text = ""
        print('logs',str(speculation_text))
        parsed_suggestions = parse_speculation_output(speculation_text)
        print('logs:', str(parsed_suggestions))
        return parsed_suggestions
    except Exception as e:
        return {"error": str(e)}