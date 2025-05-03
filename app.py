
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bol Dashboard", layout="wide")

# --- STYLING / HEADER ---
st.title("📊 Productanalyse Bol.com")
st.markdown("Een datagedreven overzicht van producten, prijsverschillen en klantinteresse.")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_excel("Top 1000 GL 2 mei 2025 .xlsx")
    df["price"] = df["price"].astype(str).str.replace("\n", "").str.replace(",", ".").str.replace("€", "")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    df["Relevante Marktprijs"] = df["Relevante Marktprijs"].astype(str).str.replace(",", ".").str.replace("€", "")
    df["Relevante Marktprijs"] = pd.to_numeric(df["Relevante Marktprijs"], errors="coerce")

    df["prijsverschil"] = df["price"] - df["Relevante Marktprijs"]
    df["procentueel_verschil"] = (df["prijsverschil"] / df["Relevante Marktprijs"]) * 100

    df["Klantbezoeken"] = df["Klantbezoeken"].astype(str).str.replace(".", "").str.replace("+", "").str.replace(",", "")
    df["Klantbezoeken"] = pd.to_numeric(df["Klantbezoeken"], errors="coerce")

    df["Productgroep"] = df["Productgroep"].fillna("Onbekend")
    return df

df = load_data()

# --- FILTERS ---
st.sidebar.header("🔎 Filters")
verkopers = st.sidebar.multiselect("Verkoper(s)", options=df["seller"].unique(), default=df["seller"].unique())
groepen = st.sidebar.multiselect("Productgroep(en)", options=df["Productgroep"].unique(), default=df["Productgroep"].unique())
min_prijs, max_prijs = st.sidebar.slider("Prijsbereik (€)", float(df["price"].min()), float(df["price"].max()), (float(df["price"].min()), float(df["price"].max())))

filtered_df = df[
    (df["seller"].isin(verkopers)) &
    (df["Productgroep"].isin(groepen)) &
    (df["price"] >= min_prijs) &
    (df["price"] <= max_prijs)
]

# --- KPI ---
col1, col2, col3 = st.columns(3)
col1.metric("Aantal producten", len(filtered_df))
col2.metric("Gem. prijsverschil", f"€{filtered_df['prijsverschil'].mean():.2f}")
col3.metric("Gem. klantbezoeken", f"{filtered_df['Klantbezoeken'].mean():.0f}")

# --- CHART 1: Scatter plot prijs vs relevante prijs ---
fig1 = px.scatter(filtered_df,
                 x="Relevante Marktprijs",
                 y="price",
                 color="Productgroep",
                 hover_data=["title", "seller", "price", "Relevante Marktprijs"],
                 title="💰 Huidige prijs vs. Relevante marktprijs")
st.plotly_chart(fig1, use_container_width=True)

# --- CHART 2: Gem. prijsverschil per productgroep ---
fig2 = px.bar(filtered_df.groupby("Productgroep")["prijsverschil"].mean().sort_values(ascending=False).reset_index(),
              x="prijsverschil", y="Productgroep", orientation="h",
              title="📉 Gemiddeld prijsverschil per productgroep")
st.plotly_chart(fig2, use_container_width=True)

# --- CHART 3: Histogram klantbezoeken ---
fig3 = px.histogram(filtered_df, x="Klantbezoeken", nbins=40,
                    title="👀 Verdeling klantbezoeken per maand")
st.plotly_chart(fig3, use_container_width=True)

# --- TABEL (max 50 per pagina) ---
st.markdown("### 📄 Productoverzicht (max 50 per pagina)")
page_size = st.selectbox("Aantal per pagina", options=[20, 30, 50], index=2)
page = st.number_input("Pagina", min_value=1, max_value=(len(filtered_df) // page_size) + 1, step=1)
start_idx = (page - 1) * page_size
end_idx = start_idx + page_size
st.dataframe(filtered_df.iloc[start_idx:end_idx].reset_index(drop=True))
