
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Zet als eerste Streamlit-aanroep
st.set_page_config(page_title="Bol.com Grey List Dashboard", layout="wide")

# Data inladen vanuit vaste paden
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_2024 = os.path.join(BASE_DIR, "data", "grey_list_dec_2024.xlsx")
file_2025 = os.path.join(BASE_DIR, "data", "top_1000_gl_2025.xlsx")

@st.cache_data
def load_all_data():
    df_2024_raw = pd.read_excel(file_2024, None)
    df_2025_raw = pd.read_excel(file_2025, None)

    df_2024 = pd.concat(df_2024_raw.values(), ignore_index=True)
    df_2025 = pd.concat(df_2025_raw.values(), ignore_index=True)

    col_2024 = next((col for col in df_2024.columns if 'category' in col.lower() and 'a' in col.lower()), None)
    col_2025 = 'Winkel' if 'Winkel' in df_2025.columns else None

    if col_2024:
        df_2024['Winkel'] = df_2024[col_2024]
    else:
        df_2024['Winkel'] = None

    if col_2025:
        df_2025['Winkel'] = df_2025[col_2025]
    else:
        df_2025['Winkel'] = None

    return df_2024, df_2025

# Load data
df_2024, df_2025 = load_all_data()

def filter_compleet_gescraped(df):
    required_cols = ["huidige_prijs", "delivery", "rating", "rating_count", "vendor"]
    return df.dropna(subset=required_cols)

# Bereken scrape stats voor beide datasets
df_2024_scraped = filter_compleet_gescraped(df_2024)
df_2025_scraped = filter_compleet_gescraped(df_2025)

totaal_2024 = df_2024.shape[0]
gescrapet_2024 = df_2024_scraped.shape[0]
scrape_rate_2024 = round((gescrapet_2024 / totaal_2024) * 100, 2)

totaal_2025 = df_2025.shape[0]
gescrapet_2025 = df_2025_scraped.shape[0]
scrape_rate_2025 = round((gescrapet_2025 / totaal_2025) * 100, 2)

# Dashboard layout
st.title("Bol.com Grey List Analyse Dashboard")

st.subheader("📦 Scrape Status Overzicht")

col1, col2, col3, col4 = st.columns(4)
col1.metric("EAN's totaal (2024)", totaal_2024)
col2.metric("Gescraped (2024)", gescrapet_2024)
col3.metric("Scrape rate (2024)", f"{scrape_rate_2024}%")

col1.metric("EAN's totaal (2025)", totaal_2025)
col2.metric("Gescraped (2025)", gescrapet_2025)
col3.metric("Scrape rate (2025)", f"{scrape_rate_2025}%")

# Je kunt hier meer visualisaties toevoegen indien nodig
