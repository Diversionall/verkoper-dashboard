
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Bepaal de paden naar de Excel-bestanden
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_2024 = os.path.join(BASE_DIR, "data", "grey_list_dec_2024.xlsx")
file_2025 = os.path.join(BASE_DIR, "data", "top_1000_gl_2025.xlsx")

# Gegevens laden
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

# Laad de data
df = load_data()

# Streamlit layout
st.set_page_config(page_title="BPA Greylist Analyse Dashboard", layout="wide")

# Sidebar navigatie
pagina = st.sidebar.radio("📂 Pagina", ["Home", "Pie Chart", "Staafdiagram"])

# Pagina 1: Home
if pagina == "Home":
    st.title("BPA Greylist Analyse Dashboard")

# Pagina 2: Pie Chart
elif pagina == "Pie Chart":
    st.title("Productverdeling per Winkel (Taartdiagram)")
    winkel_count = df['Winkel'].value_counts().reset_index()
    winkel_count.columns = ['Winkel', 'Aantal']
    fig = px.pie(winkel_count, names='Winkel', values='Aantal', title='Verdeling van producten per winkel')
    st.plotly_chart(fig, use_container_width=True)

# Pagina 3: Staafdiagram
elif pagina == "Staafdiagram":
    st.title("Staafdiagram")
    st.info("Visualisatie volgt...")
