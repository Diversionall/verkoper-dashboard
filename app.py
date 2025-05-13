
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Data inladen vanuit vaste paden
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_2024 = os.path.join(BASE_DIR, "data", "grey_list_dec_2024.xlsx")
file_2025 = os.path.join(BASE_DIR, "data", "top_1000_gl_2025.xlsx")

@st.cache_data
def load_data():
    df_2024 = pd.read_excel(file_2024, None)
    df_2025 = pd.read_excel(file_2025, None)

# === Data laden ===
df_2024, df_2025 = load_data()
df_2024_scraped = filter_compleet_gescraped(df_2024)
df_2025_scraped = filter_compleet_gescraped(df_2025)


@st.cache_data
def load_data():
    df_2024 = pd.concat(df_2024.values(), ignore_index=True)
    df_2025 = pd.concat(df_2025.values(), ignore_index=True)
    
    col_2024 = next((col for col in df_2024.columns if 'category' in col.lower() and 'a' in col.lower()), None)
    col_2025 = 'Winkel' if 'Winkel' in df_2025.columns else None
    
    df_a = df_2024[[col_2024]].rename(columns={col_2024: 'Winkel'}).dropna() if col_2024 else pd.DataFrame()
    df_b = df_2025[[col_2025]].rename(columns={col_2025: 'Winkel'}).dropna() if col_2025 else pd.DataFrame()
    
    return pd.concat([df_a, df_b], ignore_index=True)

df = load_data()

st.set_page_config(page_title="BPA Greylist Analyse Dashboard", layout="wide")

# Sidebar navigatie
pagina = st.sidebar.radio("📂 Pagina", ["Home", "Analyse", "Staafdiagram"])

# HOME
if pagina == "Home":
    st.title("BPA Greylist Analyse Dashboard")

# ANALYSE - oorspronkelijke werkende inhoud

elif pagina == "Analyse":
    st.title("📦 Scrape Analyse Overzicht")

    keuze = st.selectbox("Kies dataset", ["2024", "2025", "Beide"])
    if keuze == "2024":
        data = df_2024
        data_scraped = df_2024_scraped
    elif keuze == "2025":
        data = df_2025
        data_scraped = df_2025_scraped
    else:
        data = pd.concat([df_2024, df_2025])
        data_scraped = pd.concat([df_2024_scraped, df_2025_scraped])

    totaal = data.shape[0]
    gescrapet = data_scraped.shape[0]
    niet_gescrapet = totaal - gescrapet
    scrape_rate = round((gescrapet / totaal) * 100, 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("Totaal producten", totaal)
    col2.metric("Gescrapet (met prijs)", gescrapet)
    col3.metric("Scrape rate (%)", f"{scrape_rate}%")

    pie_df = pd.DataFrame({
        'Status': ['Gescrapet', 'Niet gescrapet'],
        'Aantal': [gescrapet, niet_gescrapet]
    })
    fig = px.pie(pie_df, names='Status', values='Aantal', title='Scrape Verdeling')
    st.plotly_chart(fig, use_container_width=True)

    # Winkelranglijst
    st.subheader("🏪 Winkelranglijst op basis van gescrapete data")
    if "Winkel" in data_scraped.columns:
        winkel_count = data_scraped["Winkel"].value_counts().reset_index()
        winkel_count.columns = ["Winkel", "Aantal"]
        winkel_count = winkel_count.sort_values(by="Aantal", ascending=False).reset_index(drop=True)
        winkel_count.index += 1

        min_val, max_val = int(winkel_count["Aantal"].min()), int(winkel_count["Aantal"].max())
        drempel = st.slider("📊 Toon winkels met minimaal aantal producten", min_val, max_val, min_val)

        gefilterd = winkel_count[winkel_count["Aantal"] >= drempel]

        for i, row in gefilterd.iterrows():
            st.markdown(f"**{i}. {row['Winkel']}** – {row['Aantal']} producten")
    else:
        st.info("Geen 'Winkel' kolom beschikbaar in de gescrapete data.")
elif pagina == "Staafdiagram":
    st.title("📊 Scrape Visualisatie per Winkel")

    keuze = st.selectbox("Kies dataset", ["2024", "2025", "Beide"])
    if keuze == "2024":
        data = df_2024_scraped
    elif keuze == "2025":
        data = df_2025_scraped
    else:
        data = pd.concat([df_2024_scraped, df_2025_scraped])

    if "Winkel" in data.columns:
        winkel_count = data["Winkel"].value_counts().reset_index()
        winkel_count.columns = ["Winkel", "Aantal"]
        winkel_count = winkel_count.sort_values(by="Aantal", ascending=False).reset_index(drop=True)
        winkel_count.index += 1  # Nummering vanaf 1

        min_val, max_val = int(winkel_count["Aantal"].min()), int(winkel_count["Aantal"].max())
        drempel = st.slider("📊 Toon winkels met minimaal aantal producten", min_val, max_val, min_val)

        gefilterd = winkel_count[winkel_count["Aantal"] >= drempel]

        fig = px.bar(gefilterd, x="Winkel", y="Aantal", title=f"Aantal producten per Winkel (min {drempel})")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🔢 Winkelranglijst")
        for i, row in gefilterd.iterrows():
            st.markdown(f"**{i}. {row['Winkel']}** – {row['Aantal']} producten")
    else:
        st.warning("Geen 'Winkel' kolom beschikbaar voor visualisatie.")

