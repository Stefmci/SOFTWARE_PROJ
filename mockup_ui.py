import streamlit as st
from datetime import datetime, timedelta



def startseite():
    st.title("Willkommen ")
    st.header("bei der Geräteverwaltung der Hochschule")
    st.write("Am linken Rand befindet sich die Navigation, wo Sie zwischen den verschiedenen Seiten wechseln können.")
    st.divider()
    st.title("News")
    st.write("Nächste Woche findet die Einschlung der CNC-Fräse statt.")
    st.divider()
    st.title("Wartungsarbeiten")
    st.write("Folgende Geräte sind nicht verfügbar.")
    st.divider()
    st.write("Bei Fragen oder Problemen wenden Sie sich bitte an den Administrator.")