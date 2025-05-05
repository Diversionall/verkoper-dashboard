import streamlit as st
import pandas as pd
import math
from detail import show_product_detail

# --- DATA LOADING ---
@st.cache_data
def load_data():
    df = pd.read_excel("Grey list mei 2025.xlsx")
    df["batch"] = "2025"
    df = df.rename(columns={
        "seller": "verkoper",
        "Winkel": "winkel",
        "artikel": "productnaam",
        "Relevante Marktprijs": "relevante_prijs",
        "Klantbezoeken": "klantbezoeken"
    })
    return df

df = load_data()

# --- ZET PRIJZEN OM NAAR NUMMERIEK ---
df["relevante_prijs"] = pd.to_numeric(df["relevante_prijs"], errors="coerce")
df["huidige_prijs"] = pd.to_numeric(df["huidige_prijs"], errors="coerce")

# --- BEREKENING ---
df = df.copy()
df = df[df["relevante_prijs"] > 0]
df["prijsverschil_%"] = ((df["huidige_prijs"] - df["relevante_prijs"]) / df["relevante_prijs"]) * 100

# --- INTERFACE ---
st.title("📊 Prijsverschil-analyse – alleen batch 2025")

# --- FILTERS ---
winkels = sorted(df["winkel"].dropna().unique())
if not winkels:
    st.warning("⚠️ Geen beschikbare winkels gevonden in de data.")
    st.stop()

gekozen_winkel = st.selectbox("🏪 Kies een hoofdcategorie (winkel):", winkels)
max_per_pagina = st.selectbox("🔢 Aantal producten per pagina:", [10, 20, 30, 40, 50, 100], index=4)
sorteer_aflopend = st.checkbox("⬇️ Sorteer op hoogste prijsverschil eerst", value=True)

# --- FILTEREN ---
filtered_df = df[df["winkel"] == gekozen_winkel]
filtered_df = filtered_df.sort_values(by="prijsverschil_%", ascending=not sorteer_aflopend)

# --- PAGINERING ---
aantal_paginas = max(1, math.ceil(len(filtered_df) / max_per_pagina))
pagina = st.number_input("📄 Ga naar pagina:", min_value=1, max_value=aantal_paginas, value=1, step=1)

start_idx = (pagina - 1) * max_per_pagina
end_idx = start_idx + max_per_pagina
pagina_df = filtered_df.iloc[start_idx:end_idx]

# --- DEBUG ---
st.write("📋 Kolommen in pagina_df:", pagina_df.columns.tolist())

# --- TABEL ---
st.markdown(f"### Resultaten voor winkel: {gekozen_winkel} (pagina {pagina}/{aantal_paginas})")
st.dataframe(
    pagina_df[[
        "productnaam", "winkel", "verkoper", "batch",
        "huidige_prijs", "relevante_prijs", "prijsverschil_%"
    ]].round(2),
    use_container_width=True
)

# --- DETAILS ---
with st.expander("🔍 Details per product (optioneel)"):
    if not pagina_df.empty:
        gekozen_product = st.selectbox("Kies een product voor detailweergave:", pagina_df["productnaam"])
        detail = pagina_df[pagina_df["productnaam"] == gekozen_product].iloc[0]
        show_product_detail(detail)
    else:
        st.info("Geen producten om te tonen op deze pagina.")