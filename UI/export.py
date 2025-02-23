import streamlit as st
import classes as cl
import matplotlib.pyplot as plt
import numpy as np
import classes as cl
import queries as qr



def datenexportieren():
    st.header("Datenexport")
    
    st.divider()
    
    st.write("Exportiere die Simulationsergebnisse.")

    mechanism_list = qr.get_all_mechanisms()

    if not mechanism_list:
        st.write("Kein Mechanismus vorhanden.")

    selected_mechanism_id = st.selectbox("Wählen Sie ein Mechanismus für den Datenexport aus!", mechanism_list, index=0)
    if ("current_mechanism" not in st.session_state or 
        st.session_state["current_mechanism"] != selected_mechanism_id):
        st.session_state["current_mechanism"] = selected_mechanism_id
        if "points" in st.session_state:
            del st.session_state["points"]
        if "connections" in st.session_state:
            del st.session_state["connections"]
        st.rerun()

    st.divider()

    mechanism = qr.load_mechanism(st.session_state["current_mechanism"])
    if not mechanism:
        st.success("Kein Mechanismus ausgewählt.")
        return
    
    # -----------------------------------
    # VISUALISIERUNG DES MECHANISMUS
    # -----------------------------------

    if not mechanism.points:
        st.warning("No points available yet.")
    else:
        placeholder = st.empty()
        visualization = cl.MechanismVisualization(st.session_state["current_mechanism"])
        
        # Punkte setzen
        visualization.points = {
            p.id: cl.Point(p.id, p.id, p.x, p.y, p.fixed) for p in mechanism.points
        }

        # Verbindungen setzen
        visualization.connections = [
            cl.Connection(f"{c.point1.id}-{c.point2.id}", visualization.points[c.point1.id], visualization.points[c.point2.id])
            for c in mechanism.connections
        ]

        # Zeichnen des Mechanismus
        visualization.plot(placeholder)


    col1, col2 = st.columns(2)
    with col1:
        if st.button("Als CSV exportieren"):
            st.success("Die CSV-Datei wird heruntergeladen!")

    with col2:
        if st.button("Als JSON exportieren"):
            st.success("Daten als JSON gespeichert!")