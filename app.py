import streamlit as st
import pandas as pd
import plotly.express as px
from detail import prepare_data, calculate_price_diff

# Set wide layout
st.set_page_config(layout="wide")
st.title("📦 Bol.com Product Dashboard")

# File upload
uploaded_file = st.file_uploader("📁 Upload Excel-bestand met Bol.com data", type=[".xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    df = prepare_data(df)
st.write("📑 Kolomnamen:", df.columns.tolist())

    # Sidebar filters
    st.sidebar.header("🔍 Filters")

    winkel = st.sidebar.multiselect("Winkel", options=sorted(df["Winkel"].dropna().unique()), default=list(df["Winkel"].dropna().unique()))
    productgroep = st.sidebar.multiselect("Productgroep", options=sorted(df["Productgroep"].dropna().unique()), default=list(df["Productgroep"].dropna().unique()))
    merknaam = st.sidebar.multiselect("Merknaam", options=sorted(df["Merknaam"].dropna().unique()), default=list(df["Merknaam"].dropna().unique()))

    rating_min = st.sidebar.slider("Minimale rating", 0.0, 5.0, 0.0, 0.1)
    rating_count_min = st.sidebar.slider("Min. aantal beoordelingen", 0, 5000, 0, 10)

    bezoeken_buckets = [
        (1000, float("inf")), (500, 1000), (250, 500), (100, 250), (75, 100),
        (50, 75), (30, 50), (0, 30)
    ]
    bezoek_labels = [
        "1.000+", "500-1.000", "250-500", "100-250", "75-100",
        "50-75", "30-50", "<30"
    ]

    # Filter data
    df_filtered = df[
        (df["Winkel"].isin(winkel)) &
        (df["Productgroep"].isin(productgroep)) &
        (df["Merknaam"].isin(merknaam)) &
        (df["rating"] >= rating_min) &
        (df["rating_count"] >= rating_count_min)
    ]

    df_filtered = calculate_price_diff(df_filtered)

    # Categorize Klantbezoeken
    def categorize_bezoeken(val):
        for i, (low, high) in enumerate(bezoeken_buckets):
            if low <= val < high:
                return bezoek_labels[i]
        return "Onbekend"

    df_filtered["BezoekCategorie"] = df_filtered["Klantbezoeken"].apply(categorize_bezoeken)

    # KPI Section
    total = len(df_filtered)
    avg_price = df_filtered["price"].mean()
    avg_diff = df_filtered["Prijsverschil"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Totaal producten", f"{total}")
    col2.metric("💶 Gemiddelde prijs", f"€ {avg_price:,.2f}")
    col3.metric("📉 Gemiddeld prijsverschil", f"€ {avg_diff:,.2f}")

    # Bar chart: producten per winkel per bezoekcategorie
    bar_data = df_filtered.groupby(["Winkel", "BezoekCategorie"]).size().reset_index(name="Aantal")
    fig = px.bar(bar_data, x="Winkel", y="Aantal", color="BezoekCategorie", barmode="stack")
    st.plotly_chart(fig, use_container_width=True)

    # Pie chart: verdeling per merknaam
    pie_data = df_filtered["Merknaam"].value_counts().reset_index()
    pie_data.columns = ["Merknaam", "Aantal"]
    fig2 = px.pie(pie_data, names="Merknaam", values="Aantal", title="Verdeling per merknaam")
    st.plotly_chart(fig2, use_container_width=True)

    # Table: prijsverschillen
    st.subheader("📋 Prijsverschil per product")
    st.dataframe(df_filtered[["Winkel", "Productgroep", "Merknaam", "price", "Relevante Marktprijs", "Prijsverschil"]].sort_values("Prijsverschil", ascending=False))

else:
    st.info("👈 Upload een Excel-bestand om te starten.")