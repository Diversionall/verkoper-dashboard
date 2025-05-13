
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Dummy data loading function
def load_data():
    return pd.DataFrame({
        'Category': ['A', 'B', 'C'],
        'Values': [100, 200, 300]
    })

st.sidebar.title("Dashboard Navigatie")
pagina = st.sidebar.radio("Ga naar", ["Home", "anals", "Overzicht"])

data = load_data()

if pagina == "Home":
    st.title("Welkom bij het Dashboard")

elif pagina == "anals":
    st.title("Analyse Pagina")

    # Eerste pie chart met genummerde legenda
    fig1, ax1 = plt.subplots()
    wedges, texts, autotexts = ax1.pie(data['Values'], autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')

    legend_labels = [f"{i+1}. {label}" for i, label in enumerate(data['Category'])]
    ax1.legend(wedges, legend_labels, title="Categorieën", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    st.pyplot(fig1)

elif pagina == "Overzicht":
    st.title("Overzichtspagina")
    st.write(data)
