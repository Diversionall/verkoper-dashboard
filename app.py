
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# === Data inladen ===
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

# === Analysepagina ===
st.title("Assortiment- en Prijsanalyse (Dashboard onderdeel 2)")

# Aantal topmerken via slider
topn = st.slider("Aantal topmerken in taartdiagram", 3, 10, 5)

# Bereken de topmerken op basis van frequentie
top_merken = df["Winkel"].value_counts().head(topn)
top_df = pd.DataFrame({
    "Winkel": top_merken.index,
    "Aantal": top_merken.values
})

# Genummerde legenda (alleen in de legenda, niet in de labels op taart)
nummering = {merk: f"{i+1}. {merk}" for i, merk in enumerate(top_df["Winkel"])}
top_df["Label"] = top_df["Winkel"].map(nummering)

# Plot met originele labels op taart, maar genummerde legenda
fig = px.pie(top_df, values="Aantal", names="Winkel", title="Top Merken in Batch Beide", 
             color_discrete_sequence=px.colors.qualitative.Set3)

# Legenda aanpassen
fig.update_traces(hovertemplate='%{label}: %{percent}', legendgroup="genummerd")
fig.update_layout(legend_title_text='Winkel (gesorteerd)', legend_traceorder='normal')
fig.for_each_trace(lambda t: t.update(name=nummering.get(t.name, t.name)))

st.plotly_chart(fig)
