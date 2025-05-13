
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Bol.com Grey List Analyse Dashboard", layout="wide")

# === Data inladen ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_2024 = os.path.join(BASE_DIR, "data", "top_1000_gl_2024.xlsx")
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

# === Data laden ===
df_2024, df_2025 = load_all_data()
df_2024_scraped = filter_compleet_gescraped(df_2024)
df_2025_scraped = filter_compleet_gescraped(df_2025)

# === Sidebar navigatie ===
pagina = st.sidebar.radio("📂 Pagina", ["Home", "Scrape Analyse", "Staafdiagram"])

# === Pagina's ===
if pagina == "Home":
    st.title("Bol.com Grey List Analyse Dashboard")
    st.markdown("Welkom op het dashboard. Navigeer via de zijbalk naar de verschillende secties.")

elif pagina == "Scrape Analyse":
    st.title("📦 Scrape Status Overzicht")

    # Selectie voor jaartal
    keuze = st.selectbox("Kies dataset", ["2024", "2025", "Beide"])
    if keuze == "2024":
        totaal = df_2024.shape[0]
        gescrapet = df_2024_scraped.shape[0]
        scrape_rate = round((gescrapet / totaal) * 100, 2)
    elif keuze == "2025":
        totaal = df_2025.shape[0]
        gescrapet = df_2025_scraped.shape[0]
        scrape_rate = round((gescrapet / totaal) * 100, 2)
    else:
        totaal = df_2024.shape[0] + df_2025.shape[0]
        gescrapet = df_2024_scraped.shape[0] + df_2025_scraped.shape[0]
        scrape_rate = round((gescrapet / totaal) * 100, 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("EAN's totaal", totaal)
    col2.metric("Gescrapet", gescrapet)
    col3.metric("Scrape rate (%)", f"{scrape_rate}%")

elif pagina == "Staafdiagram":
    st.title("📊 Scrape Visualisatie")

    keuze = st.selectbox("Kies dataset", ["2024", "2025", "Beide"])
    if keuze == "2024":
        data = df_2024_scraped
    elif keuze == "2025":
        data = df_2025_scraped
    else:
        data = pd.concat([df_2024_scraped, df_2025_scraped])

    if "Winkel" in data.columns:
        winkel_count = data["Winkel"].value_counts().reset_index()
        winkel_count.columns = ["Winkel", "Aantal"]

        fig = px.bar(winkel_count, x="Winkel", y="Aantal", title="Aantal producten per Winkel")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Geen 'Winkel' kolom beschikbaar voor visualisatie.")
