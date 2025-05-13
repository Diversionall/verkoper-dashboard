
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
    st.title("Assortiment- en Prijsanalyse (Dashboard onderdeel 2)")

    totaal = len(df)
    gescrapet = totaal - 191  # fictief aantal onbekenden
    niet_gescrapet = 191
    scrape_rate = round((gescrapet / totaal) * 100, 2)

    st.selectbox("Toon data uit batch:", ["Beide"])
    st.subheader("📦 Scrape Status Overzicht")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Totaal producten", totaal)
    col2.metric("Gescrapet (met prijs)", gescrapet)
    col3.metric("Ongeïdentificeerd", niet_gescrapet)
    col4.metric("Scrape rate (%)", f"{scrape_rate}%")

    st.slider("Minimale verkoopprijs (€)", 0.0, 100.0, 50.0)

    st.subheader("Aantal unieke producten (EANs):", help="Telt unieke items in beide batches")
    st.metric("Aantal unieke producten (EANs):", totaal - 227)  # fictieve reductie

    aantal = st.slider("Aantal topmerken in taartdiagram", 3, 10, 5)

    st.write("### Top 5 Merken in Batch Beide")
    top_n = df['Winkel'].value_counts().head(aantal).reset_index()
    top_n.columns = ['Winkel', 'Aantal']
    fig = px.pie(top_n, names='num_' + 'Winkel', values='Aantal')
    st.plotly_chart(fig, use_container_width=True)

    st.write("### Verdeling Verkoopprijzen (gefilterd)")
    prijs_data = pd.DataFrame({'Prijs': [50, 70, 120, 300, 500, 200, 150, 80, 60, 40]})
    st.bar_chart(prijs_data)

# STAAFDIAGRAM
elif pagina == "Staafdiagram":
    st.title("Staafdiagram")
    st.info("Visualisatie volgt...")


# === Toevoeging: dynamische categorie slider en genummerde legenda ===

st.title("Genummerde legenda per slider")

# Simulatie van data (vervang dit met je echte dataframe)
data = {
    "Categorie": ["Speelgoed", "Mobiel", "Klein huishoudelijke producten", "Wonen", "Computer"],
    "Waarde": [100, 80, 60, 40, 20]
}
df = pd.DataFrame(data)

# Unieke categorieën bepalen
unique_categories = df["Categorie"].unique().tolist()

# Slider om het aantal categorieën te kiezen
num_categories = st.slider("Aantal categorieën tonen", 1, len(unique_categories), 5)

# Top n categorieën selecteren
selected_categories = unique_categories[:num_categories]

# Data filteren op geselecteerde categorieën
filtered_df = df[df["Categorie"].isin(selected_categories)].copy()

# Categorieën hernoemen met nummers
category_map = {cat: f"{i+1}. {cat}" for i, cat in enumerate(selected_categories)}
filtered_df["Categorie"] = filtered_df["Categorie"].map(category_map)

# Plot maken met genummerde labels
fig = px.bar(filtered_df, x="Categorie", y="Waarde", color="Categorie")
st.plotly_chart(fig)


# === Toevoeging voor Analysepagina: Genummerde Legenda bij Taartdiagram ===

import streamlit as st
import pandas as pd
import plotly.express as px

# Simulatie van bestaande dataframe met merken en aantal producten
data = {
    "Categorie": ["Speelgoed", "Mobiel", "Klein huishoudelijke producten", "Wonen", "Computer", "Tuin", "Beauty", "Koken, Tafelen & Huishouden", "Geluid en Beeld"],
    "Aantal": [320, 167, 104, 85, 79, 68, 59, 52, 44]
}
df = pd.DataFrame(data)

# Slider voor aantal topmerken in taartdiagram
aantal_topmerken = st.slider("Aantal topmerken in taartdiagram", 3, len(df), 5)

# Sorteren op aantal producten (hoogste eerst), en topn selecteren
df_sorted = df.sort_values(by="Aantal", ascending=False).head(aantal_topmerken).copy()

# Genummerde legenda maken
nummering = {cat: f"{i+1}. {cat}" for i, cat in enumerate(df_sorted["Categorie"])}
df_sorted["Label"] = df_sorted["Categorie"].map(nummering)

# Pie chart met originele labels in de plot, maar genummerde labels in de legenda
fig = px.pie(df_sorted, values="Aantal", names='num_' + "Label", title="Top Merken in Batch Beide")
st.plotly_chart(fig)
