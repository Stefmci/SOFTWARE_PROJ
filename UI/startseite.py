import streamlit as st
import classes as cl
import matplotlib.pyplot as plt
import numpy as np


def startseite():
    st.header("Simulation ebener Mechanismen")
    st.write("Willkommen! Wähle eine Funktion in der Navigation, oder verwende die untenstehenden Buttons.")

    st.divider()

    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    
    st.markdown(
    """
    <style>
    div.stButton > button {
        font-size: 20px;
        padding: 15px 30px;
        border-radius: 10px;
        background-color: #4CAF50; /* Grün */
        color: white;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    col0, col1 = st.columns(2)

    with col0:
        if st.button("Erstellen wir einen Neuen!"):
            st.session_state["Seite"] = "Mechanismen"
            st.rerun()
    with col1:
        if st.button("Einen Bestehenden Laden!"):
            st.session_state["Seite"] = "Dateneingabe"
            st.rerun()

    st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)

    col_center = st.columns([1, 3, 1])[1]
    with col_center:
            st.image("pictures/strandbeest.jpg", caption="Strandbeest", use_container_width=True)