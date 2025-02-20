import streamlit as st
import classes as cl
import matplotlib.pyplot as plt
import numpy as np


def startseite():
    st.header("Simulation ebener Mechanismen")
    st.divider()
    st.write("In diesen Programm kannst du ebene Mechanismen simulieren und analysieren.")
    st.write("Ein ebener Mechanismus besteht aus Punkten und Verbindungen. Jeder Punkt kann sich frei bewegen oder fest sein.")
    st.write("Jede Verbindung verbindet zwei Punkte und hat eine feste Länge.")
    st.write("Die Simulation zeigt die Bewegung der Punkte und Verbindungen, wenn sich die festen Punkte bewegen.")
    st.divider()
    
    st.write("Lege los indem du auf die Registerkarte 'Mechanismen' klickst und einen Mechanismus erstellst oder lädst.")
    st.write("##### Der Klassische Viergelenkmechanismus, und das Strandbeest sind bereits vordefiniert.")
    st.header("Viel Spaß!")

    st.divider()

    col_center = st.columns([1, 3, 1])[1]
    with col_center:
            st.image("pictures/strandbeest.jpg", caption="Strandbeest", use_container_width=True)