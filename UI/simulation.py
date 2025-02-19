import streamlit as st
import classes as cl
import time
import queries as qr

def simulation():
    st.header("Simulation")
    st.divider()
    mech_list = qr.get_all_mechanismen()
    selected_mech = st.selectbox("Wähle einen Mechanismus:", mech_list if mech_list else ["Keine Mechanismen vorhanden"])
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Stop"):
            st.rerun()
    with col2:
        if st.button("Simulation starten"):
            if selected_mech and selected_mech != "Keine Mechanismen vorhanden":
                mech = qr.load_mechanismus(selected_mech)
                if mech:
                    st.success(f"Simulation für '{selected_mech}' gestartet!")
                    placeholder = st.empty()
                    plotter = cl.MechanismusVisualisierung(selected_mech, pivot_id="P1", rotating_id="P2")
                    plotter.punkte = mech.punkte
                    plotter.stangen = mech.stangen
                    plotter.store_initial_positions()
                    while True:
                        for frame in range(0, 360, 2):
                            plotter.update(frame, placeholder)
                            time.sleep(0.05)
