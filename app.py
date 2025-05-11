import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl
import os
import re

st.set_page_config(layout="wide")
st.title("📦 Assortiment- en Prijsanalyse (Dashboard onderdeel 2)")

# Bestandspaden
path_2024 = "data/grey_list_dec_2024.xlsx"
path_2025 = "data/top_1000_gl_2025.xlsx"

# Bestand-checks
missing_files = []
for path in [path_2024, path_2025]:
    if not os.path.exists(path):
        missing_files.append(path)

if missing_files:
    st.error(f"Bestand(en) niet gevonden: {', '.join(missing_files)}")
    st.stop()

# Inlezen & hernoemen
df_2024 = pd.read_excel(path_2024).rename(columns={
    'ean': 'EAN',
    'merknaam': 'Merknaam',
    'productgroep': 'Productgroep',
    'huidige_prijs': 'Prijs'
})
df_2024['Batch'] = '2024'

df_2025 = pd.read_excel(path_2025).rename(columns={
    'price': 'Prijs'
})
df_2025['Batch'] = '2025'

# Kolomharmonisatie
df = pd.concat([df_2024, df_2025], ignore_index=True)
df['Prijs'] = df['Prijs'].astype(str).str.replace("[^0-9.,]", "", regex=True)
df['Prijs'] = df['Prijs'].str.replace("\n", "", regex=False).str.replace(",", ".", regex=False)
df['Prijs'] = pd.to_numeric(df['Prijs'], errors='coerce')
df = df.dropna(subset=['Prijs'])

# Filter: batchselectie
batch_opties = ['Beide', '2024', '2025']
batch_selectie = st.selectbox("Toon data uit batch:", batch_opties)

if batch_selectie != 'Beide':
    df = df[df['Batch'] == batch_selectie]

# Filter: minimale prijs
min_prijs = st.slider("Minimale verkoopprijs (€)", min_value=0.0, max_value=float(df['Prijs'].max()), value=50.0)
df = df[df['Prijs'] >= min_prijs]

# Filter: topmerken
top_n = st.slider("Aantal topmerken in taartdiagram", min_value=3, max_value=15, value=5)
top_merknamen = df['Merknaam'].value_counts().nlargest(top_n).index
df_top = df[df['Merknaam'].isin(top_merknamen)]

# 📦 Statistiek
aantal_unieke_eans = df_top['EAN'].nunique()
st.markdown(f"### Aantal unieke producten (EANs): **{aantal_unieke_eans}**")

# 📊 Pie chart
fig_pie = px.pie(df_top, names='Merknaam',
                 title=f"Top {top_n} Merken in Batch {batch_selectie}",
                 hole=0.4)
st.plotly_chart(fig_pie, use_container_width=True)

# 📈 Histogram prijsverdeling
fig_hist = px.histogram(df, x='Prijs', nbins=30, title="Verdeling Verkoopprijzen (gefilterd)")
st.plotly_chart(fig_hist, use_container_width=True)
