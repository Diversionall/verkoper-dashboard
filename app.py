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
    # Inladen 2024
    df24 = pd.concat(pd.read_excel(FILE_2024, sheet_name=None).values(), ignore_index=True)
    df24["Jaar"] = 2024
    # Kolommen voor 2024: 'category_a' -> Winkel, 'huidige_prijs' -> price, 'vendor' -> seller
    df24 = df24.rename(columns={
        "category_a": "Winkel",
        "huidige_prijs": "price",
        "vendor": "seller"
    })

    # Inladen 2025
    df25 = pd.concat(pd.read_excel(FILE_2025, sheet_name=None).values(), ignore_index=True)
    df25["Jaar"] = 2025
    # In 2025 staan kolommen correct: Winkel, price, delivery, rating, rating_count, seller

    # Samenvoegen
    return pd.concat([df24, df25], ignore_index=True)

# Data laden
df = load_data()

# Streamlit-configuratie
st.set_page_config(page_title="BPA Greylist Analyse Dashboard", layout="wide")

# Sidebar navigatie
pagina = st.sidebar.radio("📂 Pagina", ["Home", "Analyse", "Staafdiagram"])

# 1. Home-pagina
if pagina == "Home":
    st.title("BPA Greylist Analyse Dashboard")

# 2. Analyse-pagina
elif pagina == "Analyse":
    st.title("Assortiment- en Prijsanalyse (Dashboard onderdeel 2)")

    # Dataset-selectie per jaar
    jaar_keuze = st.selectbox("Selecteer dataset:", ["Beide", "2024", "2025"])
    df_sel = df if jaar_keuze == "Beide" else df[df["Jaar"] == int(jaar_keuze)]

    # Scrape-status metrics vóór filteren op prijs
    totaal = len(df_sel)
    if jaar_keuze == "2025":
        gescrapet = df_sel[["price", "delivery", "rating", "rating_count"]].notnull().all(axis=1).sum()
    elif jaar_keuze == "2024":
        gescrapet = df_sel[["rating", "rating_count"]].notnull().all(axis=1).sum()
    else:
        df25 = df_sel[df_sel["Jaar"] == 2025]
        df24 = df_sel[df_sel["Jaar"] == 2024]
        ges25 = df25[["price", "delivery", "rating", "rating_count"]].notnull().all(axis=1).sum()
        ges24 = df24[["rating", "rating_count"]].notnull().all(axis=1).sum()
        gescrapet = ges25 + ges24
    niet_scraped = totaal - gescrapet
    scrape_rate = round(gescrapet / totaal * 100, 2) if totaal else 0

    # Toon scrape-status metrics
    st.subheader("📦 Scrape Status Overzicht")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Totaal producten", totaal)
    c2.metric("Gescrapet (met prijs)", gescrapet)
    c3.metric("Ongeïdentificeerd", niet_scraped)
    c4.metric("Scrape rate (%)", f"{scrape_rate}%")

    # Slider voor minimale verkoopprijs
    max_price = int(df_sel["price"].max()) if df_sel["price"].notnull().any() else 0
    min_price = st.slider("Minimale verkoopprijs (€)", 0, max_price, 0)
    df_sel = df_sel[df_sel["price"] >= min_price]

    # Aantal unieke producten (EANs)
    if "EAN" in df_sel.columns:
        unique_eans = df_sel["EAN"].nunique()
    else:
        unique_eans = len(df_sel)
    st.subheader("Aantal unieke producten (EANs):")
    st.metric("Aantal unieke producten (EANs)", unique_eans)

    # Slider voor aantal topwinkels in pie chart
    aantal_top = st.slider("Aantal topwinkels in taartdiagram", 3, 10, 5)

    # Genummerde pie chart voor topwinkels
    top_n = (
        df_sel["Winkel"]
        .value_counts()
        .head(aantal_top)
        .reset_index()
        .rename(columns={"index": "Winkel", "Winkel": "Aantal"})
    )
    nummering = {w: f"{i+1}. {w}" for i, w in enumerate(top_n["Winkel"])}
    top_n["Label"] = top_n["Winkel"].map(nummering)

    fig = px.pie(
        top_n,
        names="Label",
        values="Aantal",
        title="Top Winkels"
    )
    fig.update_layout(legend_title_text="Top Winkels")
    fig.update_traces(hovertemplate="%{label}<br>Aantal=%{value}")
    st.plotly_chart(fig, use_container_width=True)

# 3. Staafdiagram-pagina
elif pagina == "Staafdiagram":
    st.title("Staafdiagram")
    st.info("Visualisatie volgt...")
