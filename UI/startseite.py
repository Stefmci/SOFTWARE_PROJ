import streamlit as st
import classes as cl
import matplotlib.pyplot as plt
import numpy as np


def startseite():
    st.header("Simulation ebener Mechanismen")
    st.write("Willkommen! Wähle eine Funktion in der Navigation, oder verwende die untenstehenden Buttons.")

    st.divider()

    col_center = st.columns([1, 3, 1])[1]
    with col_center:
            st.image("pictures/strandbeest.jpg", caption="Strandbeest", use_container_width=True)