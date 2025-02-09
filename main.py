import streamlit as st
import mockup_ui as ui

st.sidebar.title("Navigation")
auswahl = st.sidebar.radio("", ["Startseite"])

if auswahl == "Startseite":
    ui.startseite()