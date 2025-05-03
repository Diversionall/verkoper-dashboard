
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Detailweergave categorie", layout="wide")

st.title("📂 Detail per hoofdcategorie")
winkel = st.query_params.get("winkel", "")

if not winkel:
    st.warning("Geen hoofdcategorie geselecteerd.")
    st.stop()

st.subheader(f"📊 Analyse voor: {winkel}")

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
    df_2024 = df_2024.rename(columns={col_2024: "klantbezoeken"})
    df_2025 = df_2025.rename(columns={col_2025: "klantbezoeken"})

    cols_common = list(set(df_2024.columns).intersection(set(df_2025.columns)))
    df = pd.concat([df_2024[cols_common], df_2025[cols_common]], ignore_index=True)

    df["klantbezoeken"] = df["klantbezoeken"].astype(str).str.replace(".", "").str.replace("+", "").str.replace(",", "")
    df["klantbezoeken"] = pd.to_numeric(df["klantbezoeken"], errors="coerce")

    def klantbezoek_klasse(x):
        if pd.isna(x): return "Onbekend"
        if x >= 1000: return "1.000+"
        elif x >= 500: return "500-1.000"
        elif x >= 250: return "250-500"
        elif x >= 100: return "100-250"
        elif x >= 75: return "75-100"
        elif x >= 50: return "50-75"
        elif x >= 30: return "30-50"
        else: return "Minder dan 30"

    df["klantbezoeksklasse"] = df["klantbezoeken"].apply(klantbezoek_klasse)

    df["relevante_prijs"] = pd.to_numeric(df.get("relevante_prijs", ""), errors="coerce")
    df["huidige_prijs"] = pd.to_numeric(df.get("huidige_prijs", ""), errors="coerce")

    return df[df["winkel"] == winkel]

data = load_data()

bar_data = data.groupby(["productgroep", "klantbezoeksklasse"]).size().reset_index(name="aantal")
bar_data["klantbezoeksklasse"] = pd.Categorical(bar_data["klantbezoeksklasse"],
    ["1.000+", "500-1.000", "250-500", "100-250", "75-100", "50-75", "30-50", "Minder dan 30", "Onbekend"],
    ordered=True)
fig_bar = px.bar(bar_data,
    x="aantal", y="productgroep", color="klantbezoeksklasse",
    orientation="h", title="Productgroepen per klantbezoeksklasse",
    color_discrete_sequence=px.colors.sequential.Blues)
st.plotly_chart(fig_bar, use_container_width=True)

if "merknaam" in data.columns:
    merkdata = data["merknaam"].value_counts().reset_index()
    merkdata.columns = ["merknaam", "aantal"]
    fig_pie = px.pie(merkdata.head(10), names="merknaam", values="aantal", title="Top 10 Merken")
    st.plotly_chart(fig_pie, use_container_width=True)

if "huidige_prijs" in data.columns and "relevante_prijs" in data.columns:
    prijsdata = data.copy()
    prijsdata = prijsdata[prijsdata["huidige_prijs"] > prijsdata["relevante_prijs"]]
    prijsdata["verschil"] = prijsdata["huidige_prijs"] - prijsdata["relevante_prijs"]
    prijsdata["% verschil"] = 100 * prijsdata["verschil"] / prijsdata["relevante_prijs"]
    st.markdown("### 💡 Producten met hogere prijs dan marktprijs")
    st.dataframe(prijsdata[["productgroep", "merknaam", "artikel", "huidige_prijs", "relevante_prijs", "verschil", "% verschil"]].sort_values("% verschil", ascending=False).head(20))
