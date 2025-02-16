import streamlit as st
import classes as cl
import matplotlib.pyplot as plt
import numpy as np


def mechanismus_verwaltung():
    
    col1, col2 = st.columns(2)
    
    with col1:
        mechanismus_id = st.text_input("Name des neuen Mechanismus", key="mechanismus_id")
        
    with col2:
        st.markdown("<div style='text-align: center;'><br></div>", unsafe_allow_html=True)
        if st.button("Speichern"):
            if mechanismus_id:
                if mechanismus_id in cl.get_all_mechanismen():
                    st.warning(f"Ein Mechanismus mit der ID '{mechanismus_id}' existiert bereits!")
                else:
                    neuer_mechanismus = cl.mechanismus(mechanismus_id)
                    cl.save_mechanismus(neuer_mechanismus)
                    st.session_state["aktueller_mechanismus"] = mechanismus_id
                    st.success(f"Mechanismus '{mechanismus_id}' gespeichert! Weiter zur Dateneingabe.")
                    st.rerun()

    st.divider()

    st.subheader("Bestehende Mechanismen")
    mechanismen_liste = cl.get_all_mechanismen()

    if not mechanismen_liste:
        st.write("Keine Mechanismen vorhanden.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:

        selected_mechanismus_id = st.selectbox("Auswählen", mechanismen_liste, index=0)
        st.session_state["aktueller_mechanismus"] = selected_mechanismus_id
        
    with col2:
        st.markdown("<div style='text-align: center;'><br></div>", unsafe_allow_html=True)
        if st.button("Löschen"):
            cl.delete_mechanismus(selected_mechanismus_id)
            st.success(f"Mechanismus '{selected_mechanismus_id}' gelöscht!")
            st.rerun()

    st.divider()

    col_links, col_rechts = st.columns([2, 3])

    with col_links:
        st.subheader("Punkte & Verbindungen")
        
        mechanismus = cl.load_mechanismus(st.session_state["aktueller_mechanismus"])
        if not mechanismus:
            st.error("Mechanismus konnte nicht geladen werden!")
            return

        if "punkte" not in st.session_state or not st.session_state["punkte"]:
            st.session_state["punkte"] = [(p.id, p.x, p.y, p.fix) for p in mechanismus.punkte.values()]

        col0, col1, col2, col3 = st.columns([2, 2, 2, 1])
        with col0:
            st.markdown("##### Punkt-ID")
        with col1:
            st.markdown("##### X-Koordinate")
        with col2:
            st.markdown("##### Y-Koordinate")
        with col3:
            st.markdown("##### Fixiert")

        neue_punkte = []
        for i, (name, x, y, fixiert) in enumerate(st.session_state["punkte"]):
            col0, col1, col2, col3 = st.columns([2, 2, 2, 1])

            with col0:
                name = st.text_input("", value=name, key=f"name_{i}")

            with col1:
                x_koordinate = st.number_input("", value=x, step=0.1, key=f"x_{i}")

            with col2:
                y_koordinate = st.number_input("", value=y, step=0.1, key=f"y_{i}")

            with col3:
                st.markdown("<div style='text-align: center;'><br></div>", unsafe_allow_html=True)
                fixiert = st.checkbox("", value=fixiert, key=f"fix_{i}")

            neue_punkte.append((name, x_koordinate, y_koordinate, fixiert))

        st.session_state["punkte"] = neue_punkte

        col0, col1, col2 = st.columns(3)

        with col0:
            if st.button("Punkt hinzufügen"):
                st.session_state["punkte"].append((f"P{len(st.session_state['punkte']) + 1}", 0.0, 0.0, False))
                st.rerun()

        with col1:
            if st.button("Alle Löschen"):
                st.session_state["punkte"] = []
                st.rerun()

        with col2:
            if st.button("Alle Speichern"):
                mechanismus.punkte = {}
                for name, x, y, fixiert in st.session_state["punkte"]:
                    mechanismus.add_point(name, x, y, fixiert)
                
                cl.save_mechanismus(mechanismus)

        st.divider()

        if "verbindungen" not in st.session_state:
            st.session_state["verbindungen"] = [(s.p1.id, s.p2.id) for s in mechanismus.stangen]

        st.write("### Verbindungen")
        if len(st.session_state["punkte"]) < 2:
            st.warning("Mindestens zwei Punkte werden benötigt, um eine Verbindung zu erstellen.")
        else:
            col1, col2, col3 = st.columns([3, 3, 2])

            with col1:
                punkt1 = st.selectbox("Punkt 1", [p[0] for p in st.session_state["punkte"]], key="punkt1")

            with col2:
                punkt2 = st.selectbox("Punkt 2", [p[0] for p in st.session_state["punkte"]], key="punkt2")

            with col3:
                if st.button("Verbindung hinzufügen"):
                    if punkt1 != punkt2:
                        neue_verbindung = (punkt1, punkt2)
                        if neue_verbindung not in st.session_state["verbindungen"] and (punkt2, punkt1) not in st.session_state["verbindungen"]:
                            st.session_state["verbindungen"].append(neue_verbindung)
                            st.rerun()
                        else:
                            st.warning("Diese Verbindung existiert bereits!")

        if st.session_state["verbindungen"]:
            for v in st.session_state["verbindungen"]:
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.write(f"🔗 {v[0]} ↔ {v[1]}")
                with col2:
                    if st.button("Löschen", key=f"del_{v}"):
                        st.session_state["verbindungen"].remove(v)
                        st.rerun()

    with col_rechts:
        st.subheader("Visualisierung")
        
        if not mechanismus.punkte:
            st.warning("Noch keine Punkte vorhanden.")
        else:
            placeholder = st.empty()
            visualisierung = cl.MechanismusVisualisierung(st.session_state["aktueller_mechanismus"])
            visualisierung.punkte = {p[0]: cl.Punkte(p[0], p[1], p[2], p[3]) for p in st.session_state["punkte"]}
            visualisierung.stangen = [cl.Stangen(v[0] + "-" + v[1], visualisierung.punkte[v[0]], visualisierung.punkte[v[1]]) for v in st.session_state["verbindungen"]]
            visualisierung.plot(placeholder)
