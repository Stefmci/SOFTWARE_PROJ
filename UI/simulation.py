import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
import queries as qr
import classes as cl

def simulation():
    st.header("Simulation")
    st.write("Matrix darstellen noch einbauen")
    st.divider()

    # Mechanismus auswählen
    mech_list = qr.get_all_mechanisms()
    selected_mech = st.selectbox("Wähle einen Mechanismus:", mech_list if mech_list else ["Keine Mechanismen vorhanden"])

    if selected_mech != "Keine Mechanismen vorhanden":
        loaded_mech = qr.load_mechanism(selected_mech)
        points_list = loaded_mech.points
    else:
        loaded_mech = None
        points_list = []

    # Animation Status verwalten
    if 'animation_status' not in st.session_state:
        st.session_state.animation_status = 'stopped'

    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Stop"):
            st.session_state.animation_status = 'paused'

    with col2:
        if st.button("Simulation starten"):
            if selected_mech != "Keine Mechanismen vorhanden":
                st.session_state.animation_status = 'running'
                st.success(f"Simulation für '{selected_mech}' gestartet!")
            else:
                st.error("Kein Mechanismus ausgewählt!")

    with col3:
        if st.button("Reset"):
            st.session_state.animation_status = 'stopped'
            st.rerun()

    placeholder = st.empty()

    if loaded_mech:

        # Alle Punkte mit `trace_point = True` finden
        trace_point_ids = [p.id for p in points_list if p.trace_point]

        # Mechanismus-Visualisierung initialisieren
        plotter = cl.MechanismVisualization(selected_mech, pivot_id="c", rotating_id="A", trace_point_ids=trace_point_ids)
        plotter.points = {p.id: p for p in loaded_mech.points}
        plotter.connections = loaded_mech.connections
        plotter.store_initial_positions()

        start_time = time.perf_counter()
        frame = 270
        while st.session_state.animation_status == 'running':
            angle = np.radians(frame)
            pts = plotter.points.values() if isinstance(plotter.points, dict) else plotter.points

            # Drehpunkt (C) und rotierender Punkt (A)
            pivot = next((p for p in pts if p.id == plotter.pivot_id or p.name == plotter.pivot_id), None)
            if pivot:
                rotating = next((p for p in pts if p.id == plotter.rotating_id or p.name == plotter.rotating_id), None)
                if rotating and rotating.id in plotter.initial_positions:
                    initial_vec = plotter.initial_positions[rotating.id] - np.array([pivot.x, pivot.y])
                    new_vec = np.array([np.cos(angle), np.sin(angle)]) * np.linalg.norm(initial_vec)
                    new_pos = np.array([pivot.x, pivot.y]) + new_vec
                    rotating.set_position(new_pos[0], new_pos[1])

            # Constraints lösen
            for _ in range(3):
                plotter.relax_constraints(1)

            # Roten Kreis um Punkt C zeichnen
            center = plotter.points.get("c")
            point_A = plotter.points.get("A")
            if center and point_A:
                radius = np.linalg.norm(np.array([point_A.x, point_A.y]) - np.array([center.x, center.y]))
                circle = plt.Circle((center.x, center.y), radius, color="red", fill=False)
                plotter.ax.add_patch(circle)

            # Mehrere Tracepunkte speichern
            for trace_id in trace_point_ids:
                trace_point = plotter.points.get(trace_id)
                if trace_point:
                    plotter.trace_paths[trace_id].append((trace_point.x, trace_point.y))


            plotter.plot(placeholder)

            frame = (frame + 2) % 360
            time.sleep(0.0005)

            # Frame berechnen
            #elapsed = time.perf_counter() - start_time
            #frame = 270 + elapsed * 20

            # Animation stoppen oder pausieren
            if st.session_state.animation_status != 'running':
                break

        if st.session_state.animation_status == 'paused':
            st.info("Animation pausiert.")
        elif st.session_state.animation_status == 'stopped':
            plotter.store_initial_positions()
            plotter.plot(placeholder)
