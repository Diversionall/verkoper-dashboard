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
    # TODO: vervang 'Category A' door de kolomnaam met winkel in 2024
    df24 = df24.rename(columns={"Category A": "Winkel"})

    # Inladen 2025
    df25 = pd.concat(pd.read_excel(FILE_2025, sheet_name=None).values(), ignore_index=True)
    df25["Jaar"] = 2025
    # In 2025 staat winkel al in kolom 'Winkel'
    # De scrape-status kolommen zijn: price, delivery, rating, rating_count

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
    if jaar_keuze != "Beide":
        df_sel = df[df["Jaar"] == int(jaar_keuze)]
    else:
        df_sel = df.copy()

    # Bereken metrics
    totaal = len(df_sel)
    if jaar_keuze == "2025":
        # 2025: product is gescrapet als alle vier kolommen gevuld zijn
        gescrapet = df_sel[["price", "delivery", "rating", "rating_count"]].notnull().all(axis=1).sum()
        niet_scraped = totaal - gescrapet
    elif jaar_keuze == "2024":
        # TODO: logica voor 2024 invullen zodra kolommen bekend zijn
        gescrapet = totaal  # placeholder
        niet_scraped = 0
    else:
        # Beide jaren
        df25 = df_sel[df_sel["Jaar"] == 2025]
        ges25 = df25[["price", "delivery", "rating", "rating_count"]].notnull().all(axis=1).sum()
        df24 = df_sel[df_sel["Jaar"] == 2024]
        ges24 = len(df24)  # placeholder
        gescrapet = ges24 + ges25
        niet_scraped = totaal - gescrapet

    scrape_rate = round(gescrapet / totaal * 100, 2) if totaal else 0

    # Scrape-status metrics
    st.subheader("📦 Scrape Status Overzicht")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Totaal producten", totaal)
    col2.metric("Gescrapet (met prijs)", gescrapet)
    col3.metric("Ongeïdentificeerd", niet_scraped)
    col4.metric("Scrape rate (%)", f"{scrape_rate}%")

    # Genummerde taartdiagram voor topwinkels
    aantal_top = st.slider("Aantal topwinkels in taartdiagram", 3, 10, 5)
    top_n = df_sel["Winkel"].value_counts().head(aantal_top).reset_index()
    top_n.columns = ["Winkel", "Aantal"]
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
