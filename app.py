
import streamlit as st
import pandas as pd

try:
    df = pd.read_csv('data.csv')  # Pas pad aan indien nodig

    # Kolom kiezen afhankelijk van dataset
    if 'Winkel' in df.columns:
        winkelkolom = 'Winkel'
    elif 'catergo_a' in df.columns:
        winkelkolom = 'catergo_a'
    else:
        raise ValueError("Geen geldige winkelkolom gevonden ('Winkel' of 'catergo_a')")

    winkel_count = df[winkelkolom].value_counts().reset_index()
    winkel_count.columns = ['Winkel', 'Aantal']

    totaal = df.shape[0]
    winkel_count['Percentage'] = round((winkel_count['Aantal'] / totaal) * 100, 2)

    st.write("### Aantal producten per winkel")
    st.bar_chart(winkel_count.set_index('Winkel')['Aantal'])

    st.write("### Percentage verdeling")
    st.bar_chart(winkel_count.set_index('Winkel')['Percentage'])

except Exception as e:
    st.error(f"Fout bij het verwerken van winkeldata: {e}")
