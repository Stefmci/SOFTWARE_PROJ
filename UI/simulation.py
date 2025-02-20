import streamlit as st
import classes as cl
import time
import queries as qr

def simulation():
    st.header("Simulation")
    
    st.write("Matrix darstellen noch einbauen")
    
    st.divider()

    mech_list = qr.get_all_mechanisms()
    selected_mech = st.selectbox("Wähle einen Mechanismus:", mech_list if mech_list else ["Keine Mechanismen vorhanden"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Stop"):
            st.rerun()
    
    mech = None
    if selected_mech and selected_mech != "Keine Mechanismen vorhanden":
        mech = qr.load_mechanism(selected_mech)
    
    if mech:
        st.subheader("Vorschau des Mechanismus")
        preview_placeholder = st.empty()
        preview_plotter = cl.MechanismVisualization(selected_mech, pivot_id="c", rotating_id="A")
        preview_plotter.points = {p.id: p for p in mech.points}
        preview_plotter.connections = mech.connections
        preview_plotter.store_initial_positions()
        preview_plotter.update(0, preview_placeholder)
    
    with col2:
        if st.button("Simulation starten"):
            if mech:
                st.success(f"Simulation für '{selected_mech}' gestartet!")
                placeholder = st.empty()
                plotter = cl.MechanismVisualization(selected_mech, pivot_id="c", rotating_id="A")
                plotter.points = {p.id: p for p in mech.points}
                plotter.connections = mech.connections
                plotter.store_initial_positions()
                
                for frame in range(0, 360, 2):
                    plotter.update(frame, placeholder)
                    time.sleep(0.05)
