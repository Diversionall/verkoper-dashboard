import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl
import os
import re

st.set_page_config(layout="wide")
st.title("🧠 BPA Product Research Dashboard")

# Bestandspaden
path_2024 = "data/grey_list_dec_2024.xlsx"
path_2025 = "data/top_1000_gl_2025.xlsx"

# Controleer bestanden
if not os.path.exists(path_2024) or not os.path.exists(path_2025):
    st.error("Eén of meerdere databestanden ontbreken in de map 'data/'.")
    st.stop()

# Data inlezen
df_2024 = pd.read_excel(path_2024).rename(columns={
    'ean': 'EAN',
    'merknaam': 'Merknaam',
    'productgroep': 'Productgroep',
    'artikel': 'Artikel',
    'huidige_prijs': 'Prijs',
    'Relevante Marktprijs': 'Marktprijs',
    'seller': 'Verkoper'
})
df_2024['Batch'] = '2024'

df_2025 = pd.read_excel(path_2025).rename(columns={
    'EAN': 'EAN',
    'Merknaam': 'Merknaam',
    'Productgroep': 'Productgroep',
    'Artikel': 'Artikel',
    'price': 'Prijs',
    'Relevante Marktprijs': 'Marktprijs',
    'seller': 'Verkoper'
})
df_2025['Batch'] = '2025'

# Combineer en standaardiseer
df = pd.concat([df_2024, df_2025], ignore_index=True)
df['Prijs'] = df['Prijs'].astype(str).str.replace("[^0-9.,]", "", regex=True).str.replace(",", ".", regex=False)
df['Marktprijs'] = df['Marktprijs'].astype(str).str.replace("[^0-9.,]", "", regex=True).str.replace(",", ".", regex=False)
df['Prijs'] = pd.to_numeric(df['Prijs'], errors='coerce')
df['Marktprijs'] = pd.to_numeric(df['Marktprijs'], errors='coerce')
df = df.dropna(subset=['Prijs'])

# Tabs
tab1, tab2, tab3 = st.tabs(["🏠 Home", "📊 Verdeling per Verkoper", "💸 Prijsverschil t.o.v. Marktprijs"])

with tab1:
    st.subheader("Greylist Analyses")

    # Statistiek
    totaal = df.shape[0]
    gescrapet = df.dropna(subset=['Prijs']).shape[0]
    ongeid = totaal - gescrapet
    rate = round((ongeid / totaal) * 100, 2)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Totaal producten", totaal)
    col2.metric("Gescrapet", gescrapet)
    col3.metric("Ongeïdentificeerd", ongeid)
    col4.metric("Scrape rate (%)", f"{rate}%")

    # Staafdiagram: productgroepen
    groep_count = df['Productgroep'].value_counts().reset_index()
    groep_count.columns = ['Productgroep', 'Aantal']
    fig_group = px.bar(groep_count.sort_values('Aantal', ascending=True), 
                       x='Aantal', y='Productgroep',
                       orientation='h', color='Aantal',
                       color_continuous_scale='Blues',
                       title="Aantal producten per productgroep (gesorteerd)")
    st.plotly_chart(fig_group, use_container_width=True)

with tab2:
    st.subheader("📊 Verdeling van verkopers (BOL vs overigen)")
    # Pie chart: bol vs anderen
    df['Bol'] = df['Verkoper'].str.lower().str.contains("bol")
    bol_count = df['Bol'].value_counts().rename({True: "Bol.com", False: "Overige verkopers"})
    pie_df = pd.DataFrame({'Verkoper': bol_count.index, 'Aantal': bol_count.values})
    pie_df['%'] = round(pie_df['Aantal'] / pie_df['Aantal'].sum() * 100, 2)
    fig = px.pie(pie_df, names='Verkoper', values='Aantal', title="Verdeling Bol vs Overigen", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("💸 Grootste prijsverschillen t.o.v. marktwaarde")

    df['Verschil (%)'] = ((df['Prijs'] - df['Marktprijs']) / df['Marktprijs']) * 100
    df = df.dropna(subset=['Marktprijs', 'Verschil (%)'])

    verkopers = df['Verkoper'].dropna().unique().tolist()
    verkoper_selectie = st.selectbox("Selecteer verkoper", verkopers)
    top_df = df[df['Verkoper'] == verkoper_selectie].sort_values('Verschil (%)', key=abs, ascending=False).head(30)

    st.dataframe(top_df[['Artikel', 'Merknaam', 'Prijs', 'Marktprijs', 'Verschil (%)']], use_container_width=True)
