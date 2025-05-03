
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Top hoofdcategorieën (1.000+)", layout="wide")

st.title("📦 Hoofdcategorieën met 1.000+ klantbezoeken – Gesorteerd")
st.markdown("Toont alleen producten met 1.000+ klantbezoeken per hoofdcategorie (winkel). Gesorteerd van meeste naar minste producten. Eén kleur in blauwe stijl.")
st.markdown("---")

@st.cache_data
def load_data():
    df_2024 = pd.read_excel("data_2024.xlsx")
    df_2025 = pd.read_excel("data_2025.xlsx")

    df_2024["winkel"] = df_2024.get("category_a", "")
    df_2025["winkel"] = df_2025.get("Winkel", "")

    def find_col(df):
        for c in df.columns:
            if c.strip().lower().replace(" ", "") == "klantbezoeken":
                return c
        return None

    col_2024 = find_col(df_2024)
    col_2025 = find_col(df_2025)
    if not col_2024 or not col_2025:
        st.error("Klantbezoekskolom ontbreekt.")
        st.stop()

    df_2024 = df_2024.rename(columns={col_2024: "klantbezoeken"})
    df_2025 = df_2025.rename(columns={col_2025: "klantbezoeken"})

    cols_common = list(set(df_2024.columns).intersection(set(df_2025.columns)))
    df = pd.concat([df_2024[cols_common], df_2025[cols_common]], ignore_index=True)

    df["klantbezoeken"] = df["klantbezoeken"].astype(str).str.replace(".", "").str.replace("+", "").str.replace(",", "")
    df["klantbezoeken"] = pd.to_numeric(df["klantbezoeken"], errors="coerce")

    def bezoeksklasse(x):
        if x >= 1000:
            return "1.000+"
        else:
            return "Other"

    df["klantbezoeksklasse"] = df["klantbezoeken"].apply(bezoeksklasse)
    df = df[df["klantbezoeksklasse"] == "1.000+"]

    grouped = df.groupby("winkel").size().reset_index(name="aantal_producten")
    grouped = grouped.sort_values("aantal_producten", ascending=False)
    grouped["winkel"] = pd.Categorical(grouped["winkel"], categories=grouped["winkel"].tolist(), ordered=True)

    return grouped

data = load_data()

fig = px.bar(data,
             x="aantal_producten",
             y="winkel",
             orientation="h",
             title="Aantal producten per hoofdcategorie (1.000+ klantbezoeken)",
             color_discrete_sequence=["#084594"],  # Donkerblauw
             labels={
                 "aantal_producten": "# Producten",
                 "winkel": "Hoofdcategorie"
             })

st.plotly_chart(fig, use_container_width=True)
