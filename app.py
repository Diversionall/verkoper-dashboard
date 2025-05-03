
import streamlit as st
import pandas as pd
import plotly.express as px

# Pagina-configuratie
st.set_page_config(page_title="Verkoper Analyse", layout="wide")

st.title("✅ Verbinding geslaagd!")
st.markdown("### Dit is een test van je interactieve dashboard.")
st.markdown("Gebruik dit als basis voor je echte visualisaties.")

# Data inladen
@st.cache_data
def load_data():
    df = pd.read_excel("Top 1000 GL 2 mei 2025 .xlsx")
    df["seller"] = df["seller"].str.strip()
    df["verkoper_type"] = df["seller"].str.lower().apply(lambda x: "Bol.com" if x == "bol.com" else "Andere verkopers")
    return df

df = load_data()

# Verdeling berekenen
verdeling = df["verkoper_type"].value_counts().reset_index()
verdeling.columns = ["Verkoper", "Aantal producten"]

# Pie chart
fig = px.pie(verdeling, values="Aantal producten", names="Verkoper",
             title="Verdeling producten: Bol.com vs Andere verkopers",
             hole=0.4)

st.plotly_chart(fig, use_container_width=True)

# Drilldown als gebruiker "Andere verkopers" kiest
st.markdown("### Klik op 'Andere verkopers' hierboven om details te zien.")
selectie = st.selectbox("Kies weergave", ["", "Toon andere verkopers"])

if selectie == "Toon andere verkopers":
    andere = df[df["verkoper_type"] == "Andere verkopers"]
    verkopers = andere["seller"].value_counts().reset_index()
    verkopers.columns = ["Verkoper", "Aantal producten"]

    st.dataframe(verkopers)

    gekozen = st.selectbox("Bekijk producten van een specifieke verkoper:", verkopers["Verkoper"].unique())
    if gekozen:
        producten = andere[andere["seller"] == gekozen]["title"].tolist()
        st.markdown(f"**Producten van {gekozen}:**")
        for p in producten:
            st.markdown(f"- {p}")
