
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Data inladen vanuit vaste paden
def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
FILE_2024 = os.path.join(BASE_DIR, "data", "grey_list_dec_2024.xlsx")
FILE_2025 = os.path.join(BASE_DIR, "data", "top_1000_gl_2025.xlsx")

@st.cache_data
def load_data():
    # Lees alle sheets in beide bestanden in en concateneer
    df_2024 = pd.concat(pd.read_excel(FILE_2024, sheet_name=None).values(), ignore_index=True)
    df_2025 = pd.concat(pd.read_excel(FILE_2025, sheet_name=None).values(), ignore_index=True)

    # Kolomnamen identificeren
    col_2024 = next((c for c in df_2024.columns if 'category' in c.lower() and 'a' in c.lower()), None)
    col_2025 = 'Winkel' if 'Winkel' in df_2025.columns else None

    # Dataframes uniformeren op kolom 'Winkel'
    df_a = df_2024[[col_2024]].rename(columns={col_2024: 'Winkel'}).dropna() if col_2024 else pd.DataFrame()
    df_b = df_2025[[col_2025]].rename(columns={col_2025: 'Winkel'}).dropna() if col_2025 else pd.DataFrame()

    return pd.concat([df_a, df_b], ignore_index=True)

# Data laden
df = load_data()

# Configuratie Streamlit
st.set_page_config(page_title="BPA Greylist Analyse Dashboard", layout="wide")

# Navigatie in sidebar
pagina = st.sidebar.radio("📂 Pagina", ["Home", "Analyse", "Staafdiagram"])

# 1. Home-pagina
if pagina == "Home":
    st.title("BPA Greylist Analyse Dashboard")

# 2. Analyse-pagina
elif pagina == "Analyse":
    st.title("Assortiment- en Prijsanalyse (Dashboard onderdeel 2)")

    # Scrape-status berekenen
    totaal = len(df)
    gescrapet = totaal - 191  # fictief onbekenden-aantal
    niet_gescrapet = 191
    scrape_rate = round((gescrapet / totaal) * 100, 2)

    # Controls & metrics
    st.selectbox("Toon data uit batch:", ["Beide"])
    st.subheader("📦 Scrape Status Overzicht")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Totaal producten", totaal)
    col2.metric("Gescrapet (met prijs)", gescrapet)
    col3.metric("Ongeïdentificeerd", niet_gescrapet)
    col4.metric("Scrape rate (%)", f"{scrape_rate}%")

    st.slider("Minimale verkoopprijs (€)", 0.0, 100.0, 50.0)

    st.subheader("Aantal unieke producten (EANs):")
    st.metric("Aantal unieke producten (EANs)", totaal - 227)

    # Taartdiagram topmerken
    aantal_topmerken = st.slider("Aantal topmerken in taartdiagram", 3, 10, 5)
    st.write("### Top Merken in Batch Beide")
    top_n = df['Winkel'].value_counts().head(aantal_topmerken).reset_index()
    top_n.columns = ['Winkel', 'Aantal']
    fig = px.pie(top_n, names='Winkel', values='Aantal')
    st.plotly_chart(fig, use_container_width=True)

    # Staafdiagram verkoopprijzen
    st.write("### Verdeling Verkoopprijzen (Demo-data)")
    prijs_data = pd.DataFrame({'Prijs': [50, 70, 120, 300, 500, 200, 150, 80, 60, 40]})
    st.bar_chart(prijs_data)

# 3. Staafdiagram-pagina
elif pagina == "Staafdiagram":
    st.title("Staafdiagram")
    st.info("Visualisatie volgt...")
