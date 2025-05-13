
import streamlit as st
import pandas as pd
import plotly.express as px
import os

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

    # Voeg winkelkolom toe
    if "category_a" in df_2024.columns:
        df_2024["Winkel"] = df_2024["category_a"]

    if "Winkel" not in df_2025.columns and "winkel" in df_2025.columns:
        df_2025["Winkel"] = df_2025["winkel"]

    return df_2024, df_2025

def filter_compleet_gescraped(df):
    # Dynamisch herkennen van kolomnamen
    alias_map = {
        "huidige_prijs": ["huidige_prijs", "price"],
        "vendor": ["vendor", "seller"]
    }
    required_fixed = ["delivery", "rating", "rating_count"]

    required_cols = []
    for key, aliases in alias_map.items():
        for alias in aliases:
            if alias in df.columns:
                required_cols.append(alias)
                break

    for col in required_fixed:
        if col in df.columns:
            required_cols.append(col)

    return df.dropna(subset=required_cols)

# Data inladen
df_2024, df_2025 = load_all_data()

# Scraping status bepalen
df_2024_scraped = filter_compleet_gescraped(df_2024)
df_2025_scraped = filter_compleet_gescraped(df_2025)

totaal_2024 = df_2024.shape[0]
gescrapet_2024 = df_2024_scraped.shape[0]
scrape_rate_2024 = round((gescrapet_2024 / totaal_2024) * 100, 2)

totaal_2025 = df_2025.shape[0]
gescrapet_2025 = df_2025_scraped.shape[0]
scrape_rate_2025 = round((gescrapet_2025 / totaal_2025) * 100, 2)

# Dashboard
st.title("Bol.com Grey List Analyse Dashboard")

st.subheader("📦 Scrape Status Overzicht")

col1, col2, col3, col4 = st.columns(4)
col1.metric("EAN's totaal (2024)", totaal_2024)
col2.metric("Gescraped (2024)", gescrapet_2024)
col3.metric("Scrape rate (2024)", f"{scrape_rate_2024}%")

col1.metric("EAN's totaal (2025)", totaal_2025)
col2.metric("Gescraped (2025)", gescrapet_2025)
col3.metric("Scrape rate (2025)", f"{scrape_rate_2025}%")
