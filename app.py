import streamlit as st
import pandas as pd

# --- DATA LOADING ---
@st.cache_data
def load_data():
    df_2024 = pd.read_excel("Grey list dec 2024.xlsx")
    df_2025 = pd.read_excel("Grey list mei 2025.xlsx")
    df_2024["batch"] = "2024"
    df_2025["batch"] = "2025"
    combined_df = pd.concat([df_2024, df_2025], ignore_index=True)
    return combined_df

df = load_data()

# --- DATA PREP ---
df = df.copy()
df = df[df["relevante_prijs"] > 0]  # voorkom deling door 0
df["prijsverschil_%"] = ((df["huidige_prijs"] - df["relevante_prijs"]) / df["relevante_prijs"]) * 100

# --- TITEL ---
st.title("📊 Prijsverschil-analyse per hoofdcategorie")

# --- FILTERS ---
hoofdcategorieën = sorted(df["hoofdcategorie"].dropna().unique())
gekozen_hoofdcategorie = st.selectbox("Kies een hoofdcategorie:", hoofdcategorieën)

gekozen_batches = st.multiselect(
    "Selecteer batchjaar/batches:",
    options=["2024", "2025"],
    default=["2024", "2025"]
)

top_n = st.selectbox("Aantal topresultaten weergeven:", options=[10, 20, 30, 40, 50], index=4)

# --- FILTER DATA ---
filtered_df = df[
    (df["hoofdcategorie"] == gekozen_hoofdcategorie) &
    (df["batch"].isin(gekozen_batches))
]

filtered_df = filtered_df.sort_values(by="prijsverschil_%", ascending=False).head(top_n)

# --- TABEL ---
st.markdown(f"### Top {top_n} producten met hoogste prijsverschil (%) – {gekozen_hoofdcategorie}")
st.dataframe(
    filtered_df[[
        "productnaam", "hoofdcategorie", "batch",
        "huidige_prijs", "relevante_prijs", "prijsverschil_%"
    ]].round(2),
    use_container_width=True
)

# --- DETAILS ---
with st.expander("🔍 Details per product (optioneel)"):
    gekozen_product = st.selectbox("Kies een product voor detailweergave:", filtered_df["productnaam"])
    detail = filtered_df[filtered_df["productnaam"] == gekozen_product].iloc[0]
    st.markdown("**Details van het geselecteerde product:**")
    st.write({
        "Productnaam": detail["productnaam"],
        "Batch": detail["batch"],
        "Hoofdcategorie": detail["hoofdcategorie"],
        "Huidige prijs": detail["huidige_prijs"],
        "Relevante marktprijs": detail["relevante_prijs"],
        "Prijsverschil (%)": round(detail["prijsverschil_%"], 2),
    })