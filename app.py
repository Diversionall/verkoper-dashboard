
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

    df["VerkoperCategorie"] = df["seller"].apply(lambda x: "Bol" if "bol" in str(x).lower() else "Overige verkopers")

    # PIE CHART + counts
    verkoper_counts = df["VerkoperCategorie"].value_counts().reset_index()
    verkoper_counts.columns = ["Verkoper", "Aantal"]

    bol_count = df[df["VerkoperCategorie"] == "Bol"].shape[0]
    overige_count = df[df["VerkoperCategorie"] == "Overige verkopers"].shape[0]

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
        st.markdown(f"**🔵 Bol producten:** {bol_count}")
        st.markdown(f"**🔴 Overige verkopers producten:** {overige_count}")

        groep_selectie = st.selectbox("🔘 Kies groep", ["Bol", "Overige verkopers"])
        filtered_df = df[df["VerkoperCategorie"] == groep_selectie]

        selected_seller = None
        if groep_selectie == "Overige verkopers":
            unique_sellers = sorted(filtered_df["seller"].unique())
            selected_seller = st.selectbox("🔍 Kies specifieke verkoper", options=unique_sellers)
            filtered_df = filtered_df[filtered_df["seller"] == selected_seller]

        # Sorting
        sort_order = st.radio("📊 Sorteer op prijs", ["Laag → Hoog", "Hoog → Laag"], horizontal=True)
        ascending = sort_order == "Laag → Hoog"
        filtered_df = filtered_df.sort_values("price", ascending=ascending)

        # Pagination
        total_products = len(filtered_df)
        page_size = 100
        total_pages = math.ceil(total_products / page_size)

        if total_products > 0:
            page = st.number_input(f"📄 Pagina (1-{total_pages})", min_value=1, max_value=total_pages, step=1)
            start = (page - 1) * page_size
            end = start + page_size
            st.write(f"**Toont producten {start+1} t/m {min(end, total_products)} van {total_products} producten.**")
            st.dataframe(filtered_df.iloc[start:end][["title", "price", "seller"]])
        else:
            st.info("Geen producten beschikbaar voor deze selectie.")

else:
    st.info("← Upload een Excel-bestand om te starten.")
