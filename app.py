
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Klantbezoek per winkelcategorie", layout="wide")

st.title("📊 Klantbezoeken per hoofdcategorie (winkel) – Gecombineerde data 2024 + 2025")
st.markdown("Aantal producten per hoofdcategorie (winkel), gesplitst naar klantbezoeksklasse per maand. Donker = veel bezoek, licht = weinig.")
st.markdown("---")

@st.cache_data
def load_data():
    df_2024 = pd.read_excel("data_2024.xlsx")
    df_2025 = pd.read_excel("data_2025.xlsx")

    df_2024["winkel"] = df_2024.get("category_a", "")
    df_2025["winkel"] = df_2025.get("Winkel", "")

    kolom_klantbezoeken = None
    for col in df_2024.columns:
        if col.strip().lower().replace(" ", "") == "klantbezoeken":
            kolom_klantbezoeken = col
            break
    if not kolom_klantbezoeken:
        for col in df_2025.columns:
            if col.strip().lower().replace(" ", "") == "klantbezoeken":
                kolom_klantbezoeken = col
                break

    if not kolom_klantbezoeken:
        st.error("❌ Kolom 'klantbezoeken' is niet gevonden in data_2024.xlsx of data_2025.xlsx.")
        st.stop()

    gemeenschappelijke_kolommen = list(set(df_2024.columns).intersection(set(df_2025.columns)))
    df_2024 = df_2024[gemeenschappelijke_kolommen]
    df_2025 = df_2025[gemeenschappelijke_kolommen]
    df = pd.concat([df_2024, df_2025], ignore_index=True)

    df[kolom_klantbezoeken] = df[kolom_klantbezoeken].astype(str).str.replace(".", "").str.replace("+", "").str.replace(",", "")
    df[kolom_klantbezoeken] = pd.to_numeric(df[kolom_klantbezoeken], errors="coerce")

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

    df["klantbezoeksklasse"] = df[kolom_klantbezoeken].apply(klantbezoek_klasse)

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
    data = df.groupby(["winkel", "klantbezoeksklasse"]).size().reset_index(name="aantal_producten")
    data["klantbezoeksklasse"] = pd.Categorical(data["klantbezoeksklasse"], categories=klasse_order, ordered=True)
    data = data.sort_values(["winkel", "klantbezoeksklasse"])
    return data

data = load_data()

fig = px.bar(data,
             x="aantal_producten",
             y="winkel",
             color="klantbezoeksklasse",
             orientation="h",
             title="Aantal producten per winkelcategorie naar klantbezoeksklasse",
             color_discrete_sequence=px.colors.sequential.Blues,
             labels={
                 "aantal_producten": "# Producten",
                 "winkel": "Hoofdcategorie",
                 "klantbezoeksklasse": "Bezoeksklasse/maand"
             })

st.plotly_chart(fig, use_container_width=True)
