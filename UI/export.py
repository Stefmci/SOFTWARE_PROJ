import streamlit as st
import classes as cl
import matplotlib.pyplot as plt
import numpy as np
import classes as cl



def datenexportieren():
    st.header("Datenexport")
    
    st.divider()
    
    st.write("Exportiere die Simulationsergebnisse.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Als CSV exportieren"):
            st.success("Daten als CSV gespeichert!")

    with col2:
        if st.button("Als JSON exportieren"):
            st.success("Daten als JSON gespeichert!")