
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Bol Product Analyse")
st.subheader("Dashboard 2025")

uploaded_file = st.file_uploader("📁 Upload Excel-bestand", type=[".xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    df.columns = df.columns.str.strip()

    # Normaliseer verkoper-categorie: "Bol.com" vs "Overige"
    df["VerkoperCategorie"] = df["seller"].apply(lambda x: "Bol" if "bol" in str(x).lower() else "Overige verkopers")

    # Tel aantal producten per verkoper-categorie
    verkoper_counts = df["VerkoperCategorie"].value_counts().reset_index()
    verkoper_counts.columns = ["Verkoper", "Aantal"]

    # Maak pie chart
    fig = px.pie(
        verkoper_counts,
        names="Verkoper",
        values="Aantal",
        color="Verkoper",
        color_discrete_map={"Bol": "blue", "Overige verkopers": "red"},
        title="Verhouding verkochte producten: Bol vs overige verkopers",
        hole=0.4
    )
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("← Upload een Excel-bestand om te starten.")
