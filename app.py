
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
    # 2024
    df24 = pd.concat(pd.read_excel(FILE_2024, sheet_name=None).values(), ignore_index=True)
    df24["Jaar"] = 2024
    # TODO: vervang 'Category A' hieronder door de juiste kolomnaam voor winkel in 2024
    df24 = df24.rename(columns={"Category A": "Winkel"})
    
    # 2025
    df25 = pd.concat(pd.read_excel(FILE_2025, sheet_name=None).values(), ignore_index=True)
    df25["Jaar"] = 2025
    # Voor 2025: 'Winkel' staat al in kolom K, dus geen herbenoemen nodig
    # Scrape-status kolommen: price, delivery, rating, rating_count

    return pd.concat([df24, df25], ignore_index=True)

df = load_data()

# Streamlit-configuratie
st.set_page_config(page_title="BPA Greylist Analyse Dashboard", layout="wide")

# Sidebar: keuze dataset
jaar_keuze = st.sidebar.selectbox("Selecteer dataset:", ["Beide", "2024", "2025"])

# Filter de data
if jaar_keuze == "Beide":
    df_sel = df
else:
    df_sel = df[df["Jaar"] == int(jaar_keuze)]

# Functie om metrics voor 2025 te berekenen
def bereken_2025_metrics(df2025):
    scraped = df2025[["price", "delivery", "rating", "rating_count"]].notnull().all(axis=1).sum()
    total = len(df2025)
    return total, scraped

# Bereken metrics per selectie
if jaar_keuze == "2025":
    totaal, gescrapet = bereken_2025_metrics(df_sel)
    niet_gescrapet = totaal - gescrapet

elif jaar_keuze == "2024":
    # TODO: implementeer hier de scraping-logica voor 2024
    totaal = len(df_sel)
    gescrapet = totaal  # placeholder
    niet_gescrapet = 0

else:  # Beide
    df24 = df_sel[df_sel["Jaar"] == 2024]
    df25 = df_sel[df_sel["Jaar"] == 2025]
    total24 = len(df24)
    total25, scraped25 = bereken_2025_metrics(df25)
    # 2024 placeholder
    scraped24 = total24
    totaal = total24 + total25
    gescrapet = scraped24 + scraped25
    niet_gescrapet = totaal - gescrapet

scrape_rate = round(gescrapet / totaal * 100, 2) if totaal > 0 else 0

# Tonen van de metrics
st.title("Assortiment- en Prijsanalyse (Dashboard onderdeel 2)")
st.subheader("📦 Scrape Status Overzicht")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Totaal producten", totaal)
col2.metric("Gescrapet (met prijs)", gescrapet)
col3.metric("Ongeïdentificeerd", niet_gescrapet)
col4.metric("Scrape rate (%)", f"{scrape_rate}%")

# Taartdiagram topwinkels met genummerde legenda
aantal_top = st.slider("Aantal topwinkels in taartdiagram", 3, 10, 5)
top_n = df_sel['Winkel'].value_counts().head(aantal_top).reset_index()
top_n.columns = ['Winkel', 'Aantal']
nummering = {w: f"{i+1}. {w}" for i, w in enumerate(top_n['Winkel'])}
top_n['Label'] = top_n['Winkel'].map(nummering)

fig = px.pie(top_n, names='Label', values='Aantal', title="Top Winkels")
fig.update_layout(legend_title_text="Top Winkels")
fig.update_traces(hovertemplate='%{label}<br>Aantal=%{value}')
st.plotly_chart(fig, use_container_width=True)

