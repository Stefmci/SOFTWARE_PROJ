import streamlit as st
import classes as cl
import matplotlib.pyplot as plt
import numpy as np
import classes as cl



def simulation():
    st.header("Simulation")
    
    st.divider()
    
    mech_list = cl.get_all_mechanismen()
    selected_mech = st.selectbox("Wähle einen Mechanismus:", mech_list if mech_list else ["Keine Mechanismen vorhanden"])

    if st.button("Simulation starten"):
        if selected_mech and selected_mech != "Keine Mechanismen vorhanden":
            mech = cl.load_mechanismus(selected_mech)
            if mech:
                st.success(f"Simulation für '{selected_mech}' gestartet!")
                placeholder = st.empty()
                plotter = cl.MechanismusVisualisierung(selected_mech)
                plotter.plot(placeholder)
                plotter.animate(placeholder)

    if st.session_state.button_clicked:
        st.error("Achtung: Der Button wurde gedrückt!")