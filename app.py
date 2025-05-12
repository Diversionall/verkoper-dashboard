
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide")
st.title("🧠 BPA Product Research Dashboard")

# Sidebar navigatie
pagina = st.sidebar.radio("📁 Kies dashboardonderdeel:", [
    "🏠 Home", 
    "📊 Verdeling per Verkoper", 
    "💸 Prijsverschil t.o.v. Marktprijs"
])

# Laad data
path_2024 = "data/grey_list_dec_2024.xlsx"
path_2025 = "data/top_1000_gl_2025.xlsx"

df_2024 = pd.read_excel(path_2024)
df_2025 = pd.read_excel(path_2025)

# Voorbereiden winkelkolommen
df_2024['category_a'] = df_2024['category_a'].replace("Koken & Tafelen", "Koken, Tafelen & Huishouden")
df_2025['Winkel'] = df_2025['Winkel'].replace("Koken & Tafelen", "Koken, Tafelen & Huishouden")

df_2024['Winkel'] = df_2024['category_a']
df_2024['Batch'] = '2024'
df_2025['Batch'] = '2025'

df = pd.concat([df_2024, df_2025], ignore_index=True)

# Pagina 1
if pagina == "🏠 Home":
    st.subheader("Greylist Analyses")

    totaal = df.shape[0]
    gescrapet = df.dropna(subset=['Prijs']).shape[0] if 'Prijs' in df.columns else totaal
    col1, col2 = st.columns(2)
    col1.metric("Totaal producten", totaal)
    col2.metric("Gescrapet", gescrapet)

    # Staafdiagram: producten per winkel
    winkel_count = df['Winkel'].value_counts().rename_axis('Winkel').reset_index(name='Aantal')
    totaal = df.shape[0]
    winkel_count['Percentage'] = round((winkel_count['Aantal'] / totaal) * 100, 2)
    winkel_count.columns = ['Winkel', 'Aantal']
    winkel_count = winkel_count.sort_values('Aantal', ascending=True)

    fig = px.bar(
        winkel_count,
        winkel_count,
        x='Aantal',
        y='Winkel',
        orientation='h',
        title="Aantal producten per winkel (gesorteerd)",
        hover_data=['Aantal', 'Percentage'],
        color_discrete_sequence=["rgba(135,206,250,0.6)"]
    )
    fig.update_layout(width=1000, height=700)
    st.plotly_chart(fig, use_container_width=False)

# Pagina 2 placeholder
elif pagina == "📊 Verdeling per Verkoper":
    st.subheader("📊 Hier komt de verdeling per verkoper (volgende stap)")

# Pagina 3 placeholder
elif pagina == "💸 Prijsverschil t.o.v. Marktprijs":
    st.subheader("💸 Hier komt de prijsanalyse t.o.v. marktprijs (volgende stap)")
