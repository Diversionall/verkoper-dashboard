
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Top hoofdcategorieën (1.000+)", layout="wide")

st.title("📦 Hoofdcategorieën met 1.000+ klantbezoeken – Klik voor detail")
st.markdown("Klik op een balk om een detailweergave per hoofdcategorie te openen.")
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

    df["klantbezoeksklasse"] = df["klantbezoeken"].apply(lambda x: "1.000+" if x >= 1000 else "Other")
    df = df[df["klantbezoeksklasse"] == "1.000+"]

    grouped = df.groupby("winkel").size().reset_index(name="aantal_producten")
    grouped = grouped.sort_values("aantal_producten", ascending=True)
    grouped["winkel"] = pd.Categorical(grouped["winkel"], categories=grouped["winkel"].tolist(), ordered=True)

    return grouped

data = load_data()

fig = px.bar(data,
             x="aantal_producten",
             y="winkel",
             orientation="h",
             title="Aantal producten per hoofdcategorie (1.000+ klantbezoeken)",
             color_discrete_sequence=["#084594"],
             labels={"aantal_producten": "# Producten", "winkel": "Hoofdcategorie"},
             custom_data=["winkel"])

fig.update_traces(
    hovertemplate="<b>%{customdata[0]}</b><br>Aantal producten: %{x}",
    marker_line_width=0,
)

fig.update_layout(clickmode='event+select')

selected = st.plotly_chart(fig, use_container_width=True)

st.markdown("ℹ️ Klik op een categorie hierboven om de detailpagina te openen.")

if st.session_state.get("plotly_click_event"):
    selected_winkel = st.session_state["plotly_click_event"]["points"][0]["customdata"][0]
    st.experimental_set_query_params(winkel=selected_winkel)
    st.experimental_rerun()
