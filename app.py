
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Klantbezoek per winkel", layout="wide")

st.title("📊 Winkelanalyse: klantbezoeken per maand")
st.markdown("Overzicht van het aantal producten per winkel, gecategoriseerd op aantal maandelijkse klantbezoeken.")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_excel("Top 1000 GL 2 mei 2025 .xlsx")

    df["Klantbezoeken"] = df["Klantbezoeken"].astype(str).str.replace(".", "").str.replace("+", "").str.replace(",", "")
    df["Klantbezoeken"] = pd.to_numeric(df["Klantbezoeken"], errors="coerce")

    def klantbezoek_klasse(aantal):
        if pd.isna(aantal):
            return "Onbekend"
        if aantal >= 1000:
            return "1.000+"
        elif aantal >= 500:
            return "500-1.000"
        elif aantal >= 250:
            return "250-500"
        elif aantal >= 100:
            return "100-250"
        elif aantal >= 75:
            return "75-100"
        elif aantal >= 50:
            return "50-75"
        elif aantal >= 30:
            return "30-50"
        else:
            return "Minder dan 30"

    df["klantbezoeksklasse"] = df["Klantbezoeken"].apply(klantbezoek_klasse)
    return df

df = load_data()

# Data groeperen voor stacked bar
stacked_data = df.groupby(["Winkel", "klantbezoeksklasse"]).size().reset_index(name="aantal_producten")

klasse_order = [
    "1.000+",
    "500-1.000",
    "250-500",
    "100-250",
    "75-100",
    "50-75",
    "30-50",
    "Minder dan 30",
    "Onbekend"
]
stacked_data["klantbezoeksklasse"] = pd.Categorical(stacked_data["klantbezoeksklasse"], categories=klasse_order, ordered=True)
stacked_data = stacked_data.sort_values(["Winkel", "klantbezoeksklasse"])

# Visualisatie
fig = px.bar(stacked_data,
             x="Winkel",
             y="aantal_producten",
             color="klantbezoeksklasse",
             title="Stacked bar: Aantal producten per winkel naar klantbezoeksklasse",
             labels={"aantal_producten": "# Producten", "Winkel": "Winkel", "klantbezoeksklasse": "Klantbezoeken/maand"})

st.plotly_chart(fig, use_container_width=True)
