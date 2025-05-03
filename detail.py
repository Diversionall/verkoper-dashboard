import streamlit as st

def show_product_detail(product_row):
    st.markdown("**Details van het geselecteerde product:**")
    st.write({
        "Productnaam": product_row["productnaam"],
        "Batch": product_row["batch"],
        "Winkel": product_row["winkel"],
        "Huidige prijs": product_row["huidige_prijs"],
        "Relevante marktprijs": product_row["relevante_prijs"],
        "Prijsverschil (%)": round(product_row["prijsverschil_%"], 2),
    })