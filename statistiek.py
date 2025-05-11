import streamlit as st
import pandas as pd
import openpyxl
import os

st.set_page_config(layout="wide")
st.title("📊 Scrape Status Overzicht per Batch")

# Bestandspaden
path_2024 = "data/grey_list_dec_2024.xlsx"
path_2025 = "data/top_1000_gl_2025.xlsx"

# Batchselectie
batch_optie = st.selectbox("Selecteer batch", ["Beide", "2024", "2025"])

def analyse_batch(pad, kolom):
    df = pd.read_excel(pad)
    totaal = df.shape[0]
    df[kolom] = df[kolom].astype(str).str.replace("[^0-9.,]", "", regex=True)
    df[kolom] = df[kolom].str.replace("\n", "", regex=False).str.replace(",", ".", regex=False)
    df[kolom] = pd.to_numeric(df[kolom], errors='coerce')
    gescrapet = df.dropna(subset=[kolom]).shape[0]
    mislukt = totaal - gescrapet
    percentage = round((mislukt / totaal) * 100, 2)
    return totaal, gescrapet, mislukt, percentage

# Analyse per selectie
if batch_optie == "2024":
    totaal, gescrapet, mislukt, percentage = analyse_batch(path_2024, "huidige_prijs")
    st.subheader("Batch 2024")
    st.metric("Totaal aantal producten", totaal)
    st.metric("Aantal gescrapet", gescrapet)
    st.metric("Aantal mislukt", mislukt)
    st.metric("Percentage mislukt", f"{percentage}%")

elif batch_optie == "2025":
    totaal, gescrapet, mislukt, percentage = analyse_batch(path_2025, "price")
    st.subheader("Batch 2025")
    st.metric("Totaal aantal producten", totaal)
    st.metric("Aantal gescrapet", gescrapet)
    st.metric("Aantal mislukt", mislukt)
    st.metric("Percentage mislukt", f"{percentage}%")

else:
    totaal_2024, gescrapet_2024, mislukt_2024, _ = analyse_batch(path_2024, "huidige_prijs")
    totaal_2025, gescrapet_2025, mislukt_2025, _ = analyse_batch(path_2025, "price")

    totaal = totaal_2024 + totaal_2025
    gescrapet = gescrapet_2024 + gescrapet_2025
    mislukt = mislukt_2024 + mislukt_2025
    percentage = round((mislukt / totaal) * 100, 2)

    st.subheader("Beide Batches")
    st.metric("Totaal aantal producten", totaal)
    st.metric("Aantal gescrapet", gescrapet)
    st.metric("Aantal mislukt", mislukt)
    st.metric("Percentage mislukt", f"{percentage}%")
