import streamlit as st
import pandas as pd
import math
from detail import show_product_detail

# --- DATA LOADING ---
@st.cache_data
def load_data():
    df_2024 = pd.read_excel("Grey list dec 2024.xlsx")
    df_2025 = pd.read_excel("Grey list mei 2025.xlsx")
    df_2024["batch"] = "2024"
    df_2025["batch"] = "2025"

    # Harmoniseer kolomnamen
    df_2024 = df_2024.rename(columns={
        "vender": "verkoper",
        "Category A": "winkel",
        "productgroep": "productgroep_2024"
    })

    df_2025 = df_2025.rename(columns={
        "seller": "verkoper",
        "Winkel": "winkel",
        "productgroep": "productgroep_2025"
    })

    # Voeg de dataframes samen
    combined_df = pd.concat([df_2024, df_2025], ignore_index=True)
    return combined_df

df = load_data()

# --- CONTROLE EN BEREKENINGEN ---
df = df.copy()
df = df[df["relevante_prijs"] > 0]
df["prijsverschil_%"] = ((df["huidige_prijs"] - df["relevante_prijs"]) / df["relevante_prijs"]) * 100

# --- INTERFACE ---
st.title("📊 Prijsverschil-analyse per hoofdcategorie (winkel)")

# --- FILTERS ---
batch_keuze = st.multiselect("📅 Selecteer batchjaar/batches:", ["2024", "2025"], default=["2024", "2025"])
winkels = sorted(df["winkel"].dropna().unique())
gekozen_winkel = st.selectbox("🏪 Kies een hoofdcategorie (winkel):", winkels)

max_per_pagina = st.selectbox("🔢 Aantal producten per pagina:", [10, 20, 30, 40, 50, 100], index=4)
sorteer_aflopend = st.checkbox("⬇️ Sorteer op hoogste prijsverschil eerst", value=True)

# --- FILTER DATA ---
filtered_df = df[(df["batch"].isin(batch_keuze)) & (df["winkel"] == gekozen_winkel)]
filtered_df = filtered_df.sort_values(by="prijsverschil_%", ascending=not sorteer_aflopend)

# --- PAGINERING ---
aantal_paginas = max(1, math.ceil(len(filtered_df) / max_per_pagina))
pagina = st.number_input("📄 Ga naar pagina:", min_value=1, max_value=aantal_paginas, value=1, step=1)

start_idx = (pagina - 1) * max_per_pagina
end_idx = start_idx + max_per_pagina
pagina_df = filtered_df.iloc[start_idx:end_idx]

# --- DEBUG: kolomnamen tonen ---
st.write("📋 Kolommen in pagina_df:", pagina_df.columns.tolist())

# --- TABEL ---
st.markdown(f"### Resultaten voor winkel: {gekozen_winkel} (pagina {pagina}/{aantal_paginas})")
st.dataframe(
    pagina_df[[
        "artikel", "winkel", "verkoper", "batch",
        "huidige_prijs", "relevante_prijs", "prijsverschil_%"
    ]].rename(columns={"artikel": "productnaam"}).round(2),
    use_container_width=True
)

# --- DETAILS ---
with st.expander("🔍 Details per product (optioneel)"):
    if not pagina_df.empty:
        gekozen_product = st.selectbox("Kies een product voor detailweergave:", pagina_df["artikel"])
        detail = pagina_df[pagina_df["artikel"] == gekozen_product].iloc[0]
        show_product_detail(detail)
    else:
        st.info("Geen producten om te tonen op deze pagina.")