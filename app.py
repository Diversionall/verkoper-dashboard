
import pandas as pd
import plotly.express as px
import streamlit as st

# Functie om data uit 2024 en 2025 te laden en combineren met optionele upload
def load_and_combine_data(uploaded_file=None):
    df_combined = pd.DataFrame()

    # Hardcoded bestanden
    df_2024 = pd.read_excel("grey_list_dec_2024.xlsx", None)
    df_2025 = pd.read_excel("top_1000_gl_2025.xlsx", None)

    df_2024 = pd.concat(df_2024.values(), ignore_index=True)
    df_2025 = pd.concat(df_2025.values(), ignore_index=True)

    # Kolom detectie
    col_2024 = next((col for col in df_2024.columns if 'category' in col.lower() and 'a' in col.lower()), None)
    col_2025 = 'Winkel' if 'Winkel' in df_2025.columns else None

    df_a = df_2024[[col_2024]].rename(columns={col_2024: 'Winkel'}).dropna() if col_2024 else pd.DataFrame()
    df_b = df_2025[[col_2025]].rename(columns={col_2025: 'Winkel'}).dropna() if col_2025 else pd.DataFrame()

    df_combined = pd.concat([df_a, df_b], ignore_index=True)

    # Extra bestand van upload
    if uploaded_file:
        df_uploaded = pd.read_excel(uploaded_file, None)
        df_uploaded = pd.concat(df_uploaded.values(), ignore_index=True)
        col_uploaded = next((col for col in df_uploaded.columns if 'winkel' in col.lower() or ('category' in col.lower() and 'a' in col.lower())), None)
        if col_uploaded:
            df_extra = df_uploaded[[col_uploaded]].rename(columns={col_uploaded: 'Winkel'}).dropna()
            df_combined = pd.concat([df_combined, df_extra], ignore_index=True)

    return df_combined

# Streamlit pagina setup
st.set_page_config(page_title="BPA Greylist Analyse Dashboard", layout="wide")

# Sidebar navigatie
pagina = st.sidebar.radio("📂 Pagina", ["Home", "Pie Chart", "Staafdiagram"])

# Bestand upload
uploaded_file = st.sidebar.file_uploader("📤 Upload extra Excel-bestand", type=["xlsx"])

# Laad gecombineerde data
df = load_and_combine_data(uploaded_file)

# HOME PAGE
if pagina == "Home":
    st.title("BPA Greylist Analyse Dashboard")

# PIE CHART
elif pagina == "Pie Chart":
    st.title("Productverdeling per Winkel (Taartdiagram)")
    winkel_count = df['Winkel'].value_counts().reset_index()
    winkel_count.columns = ['Winkel', 'Aantal']

    fig = px.pie(winkel_count, names='Winkel', values='Aantal', title='Verdeling van producten per winkel')
    st.plotly_chart(fig, use_container_width=True)

# STAAFDIAGRAM
elif pagina == "Staafdiagram":
    st.title("Productaantallen per Winkel (Staafdiagram)")

    winkel_count = df['Winkel'].value_counts().reset_index()
    winkel_count.columns = ['Winkel', 'Aantal']
    winkel_count = winkel_count.sort_values('Aantal', ascending=False)

    # Blauw kleurverloop van licht naar donker blauw
    n = len(winkel_count)
    colors = [f"rgba(0,0,255,{0.3 + 0.7*i/n})" for i in range(n)]

    fig = px.bar(
        winkel_count,
        x='Aantal',
        y='Winkel',
        orientation='h',
        color_discrete_sequence=["blue"] * n
    )

    # Pas individuele kleuren toe met gradient effect
    fig.update_traces(marker=dict(color=colors))

    fig.update_layout(
        yaxis=dict(categoryorder='total ascending'),
        height=600,
        title="Aantal producten per winkel",
        margin=dict(l=50, r=50, t=50, b=50)
    )

    st.plotly_chart(fig, use_container_width=True)
