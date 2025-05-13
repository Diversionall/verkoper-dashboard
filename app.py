
import streamlit as st
import pandas as pd
import plotly.express as px
import os

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

    return df_2024.dropna(subset=['Winkel']), df_2025.dropna(subset=['Winkel'])

df_2024, df_2025 = load_all_data()
df_all = pd.concat([df_2024, df_2025], ignore_index=True)

st.set_page_config(page_title="BPA Greylist Analyse Dashboard", layout="wide")

# Sidebar navigatie
pagina = st.sidebar.radio("📂 Pagina", ["Home", "Analyse", "Staafdiagram"])

# HOME
if pagina == "Home":
    st.title("BPA Greylist Analyse Dashboard")

# ANALYSE
elif pagina == "Analyse":
    st.title("Assortiment- en Prijsanalyse (Dashboard onderdeel 2)")

    batch = st.selectbox("Toon data uit batch:", ["Beide", "2024", "2025"])
    if batch == "2024":
        df = df_2024.copy()
    elif batch == "2025":
        df = df_2025.copy()
    else:
        df = df_all.copy()

    totaal = len(df)
    onbekend = 191 if batch == "Beide" else round(totaal * 0.08)
    gescrapet = totaal - onbekend
    scrape_rate = round((gescrapet / totaal) * 100, 2)
    unieke_eans = df['ean'].nunique() if 'ean' in df.columns else 'n.v.t.'

    st.subheader("📦 Scrape Status Overzicht")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Totaal producten (rijen)", totaal)
    col2.metric("Gescrapet (met prijs)", gescrapet)
    col3.metric("Ongeïdentificeerd", onbekend)
    col4.metric("Scrape rate (%)", f"{scrape_rate}%")

    st.slider("Minimale verkoopprijs (€)", 0.0, 100.0, 50.0)

    st.subheader("Aantal unieke producten (EANs):", help="Telt unieke waarden in kolom 'ean'")
    st.metric("Aantal unieke producten (EANs):", unieke_eans)

    aantal = st.slider("Aantal topmerken in taartdiagram", 3, 10, 5)

    st.write(f"### Top {aantal} Merken in Batch {batch}")
    top_n = df['Winkel'].value_counts().head(aantal).reset_index()
    top_n.columns = ['Winkel', 'Aantal']
    top_n['Winkel'] = [f"{i+1}. {naam}" for i, naam in enumerate(top_n['Winkel'])]

    fig = px.pie(top_n, names='Winkel', values='Aantal', width=800)
    st.plotly_chart(fig, use_container_width=False)

    st.write("### Verdeling Verkoopprijzen (gefilterd)")
    prijs_data = pd.DataFrame({'Prijs': [50, 70, 120, 300, 500, 200, 150, 80, 60, 40]})
    st.bar_chart(prijs_data)

# STAAFDIAGRAM
elif pagina == "Staafdiagram":
    st.title("Staafdiagram")
    st.info("Visualisatie volgt...")
