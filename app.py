import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl
import re

st.set_page_config(layout="wide")
st.title("BOL.com Dashboard")

uploaded_file = st.file_uploader("Upload Excel-bestand", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("Voorbeelddata")
    st.dataframe(df.head())

    # Verwerk prijsveld: haal alleen getallen eruit en converteer naar float
    df['price'] = df['price'].astype(str).str.replace("[^0-9.,]", "", regex=True)
    df['price'] = df['price'].str.replace("\n", "", regex=False).str.replace(",", ".", regex=False)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna(subset=['price'])

    # Interactieve filter: minimumprijs selecteren
    min_price = st.slider("Minimale verkoopprijs (€)", min_value=0.0, max_value=float(df['price'].max()), value=50.0)
    df_filtered = df[df['price'] >= min_price]

    # Interactieve selectie: top N merken
    top_n = st.slider("Aantal topmerken in taartdiagram", min_value=3, max_value=15, value=5)
    top_brands = df_filtered['Merknaam'].value_counts().nlargest(top_n)
    df_top_brands = df_filtered[df_filtered['Merknaam'].isin(top_brands.index)]

    # Pie chart: Aantal producten per merk
    fig_pie = px.pie(
        df_top_brands,
        names='Merknaam',
        title=f"Top {top_n} Merken (producten ≥ €{min_price:.2f})",
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Extra: Histogram van verkoopprijzen
    if "price" in df.columns:
        fig = px.histogram(df_filtered, x="price", nbins=30, title="Verdeling Verkoopprijzen (gefilterd)")
        st.plotly_chart(fig, use_container_width=True)
