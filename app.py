
import streamlit as st
import pandas as pd
import plotly.express as px
import math

st.set_page_config(layout="wide")
st.title("📊 Bol Product Analyse")
st.subheader("Dashboard 2025")

uploaded_file = st.file_uploader("📁 Upload Excel-bestand", type=[".xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    df.columns = df.columns.str.strip()

    # Categoriseer verkopers
    df["VerkoperCategorie"] = df["seller"].apply(lambda x: "Bol" if "bol" in str(x).lower() else "Overige verkopers")

    # PIE CHART
    verkoper_counts = df["VerkoperCategorie"].value_counts().reset_index()
    verkoper_counts.columns = ["Verkoper", "Aantal"]
    col1, col2 = st.columns([2, 1])
    with col1:
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

    with col2:
        selected = st.selectbox("🔘 Kies verkoper voor productdetails", verkoper_counts["Verkoper"])
        verkoper_df = df[df["VerkoperCategorie"] == selected].reset_index(drop=True)
        total_products = len(verkoper_df)
        page_size = 100
        total_pages = math.ceil(total_products / page_size)

        st.write(f"**{selected} heeft {total_products} producten.**")
        st.write(f"**Aantal pagina's: {total_pages} (100 per pagina)**")

        if total_products > 0:
            page = st.number_input(f"Pagina (1-{total_pages})", min_value=1, max_value=total_pages, step=1)
            start = (page - 1) * page_size
            end = start + page_size
            st.write(f"**Toont producten {start+1} t/m {min(end, total_products)}**")
            st.dataframe(verkoper_df.iloc[start:end][["title", "price", "seller"]])
        else:
            st.info("Geen producten beschikbaar voor deze verkoper.")

else:
    st.info("← Upload een Excel-bestand om te starten.")
