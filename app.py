
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

    def parse_price(val):
        try:
            if pd.isna(val):
                return None
            return float(
                str(val)
                .replace("€", "")
                .replace(".", "")
                .replace(",", ".")
                .replace("\n", "")
                .strip()
            )
        except:
            return None

    df["price"] = df["price"].apply(parse_price)
    df["Relevante Marktprijs"] = df["Relevante Marktprijs"].apply(parse_price)
    df["rating"] = pd.to_numeric(df["rating"].astype(str).str.replace(",", "."), errors="coerce")
    df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce")

    df["VerkoperCategorie"] = df["seller"].apply(lambda x: "Bol" if "bol" in str(x).lower() else "Overige verkopers")

    st.header("1️⃣ Verkoopsverdeling & Verkoperanalyse")

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

        if groep_selectie == "Overige verkopers":
            unique_sellers = sorted(filtered_df["seller"].dropna().unique())
            selected_seller = st.selectbox("🔍 Kies individuele verkoper", unique_sellers)
            filtered_df = filtered_df[filtered_df["seller"] == selected_seller]

        sort_order = st.radio("📊 Sorteer op prijs", ["Laag → Hoog", "Hoog → Laag"], horizontal=True)
        ascending = sort_order == "Laag → Hoog"
        filtered_df = filtered_df.sort_values("price", ascending=ascending)

        total_products = len(filtered_df)
        page_size = 100
        total_pages = max(1, math.ceil(total_products / page_size))
        page = st.number_input(f"📄 Pagina (1-{total_pages})", min_value=1, max_value=total_pages, step=1)
        start = (page - 1) * page_size
        end = start + page_size
        st.write(f"**Toont producten {start+1} t/m {min(end, total_products)} van {total_products} producten.**")
        st.write(f"🔢 Aantal producten in lijst: {total_products}")
        st.dataframe(filtered_df.iloc[start:end][["title", "price", "seller"]])

    st.markdown("<hr><br><br>", unsafe_allow_html=True)

    st.header("2️⃣ Winkelanalyse & Prijsverschillen")

    df["Prijsverschil%"] = ((df["Relevante Marktprijs"] - df["price"]) / df["Relevante Marktprijs"]) * 100
    df["Prijsverschil%"] = df["Prijsverschil%"].round(2)

    winkels = sorted(df["Winkel"].dropna().unique())
    winkel_selectie = st.selectbox("🏬 Kies winkel", winkels)

    rating = st.slider("⭐ Minimale rating", 0.0, 5.0, 0.0, 0.1)
    min_reviews = st.slider("📊 Minimaal aantal reviews", 0, 1000, 0, step=10)

    winkel_df = df[
        (df["Winkel"] == winkel_selectie) &
        (df["rating"] >= rating) &
        (df["rating_count"] >= min_reviews)
    ].copy()

    winkel_df = winkel_df.sort_values("Prijsverschil%", ascending=False)

    total_winkel = len(winkel_df)
    pagina_grootte = 50
    totaal_paginas = max(1, math.ceil(total_winkel / pagina_grootte))
    pagina = st.number_input(f"📃 Pagina (1-{totaal_paginas})", min_value=1, max_value=totaal_paginas, step=1)
    start_idx = (pagina - 1) * pagina_grootte
    eind_idx = start_idx + pagina_grootte

    st.write(f"**Toont producten {start_idx+1} t/m {min(eind_idx, total_winkel)} van {total_winkel} producten.**")
    if total_winkel > 0:
        st.write(f"🔢 Aantal producten in lijst: {total_winkel}")
        st.dataframe(
            winkel_df.iloc[start_idx:eind_idx][["title", "price", "Relevante Marktprijs", "Prijsverschil%", "rating", "rating_count", "EAN"]]
        )
    else:
        st.warning("Geen producten gevonden met deze filters.")

else:
    st.info("← Upload een Excel-bestand om te starten.")
