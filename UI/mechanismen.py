import streamlit as st
import classes as cl
import queries as qr

def mechanismus_verwaltung():
    st.subheader("Mechanismus Verwaltung")
    st.divider()
    
    mechanismen_liste = qr.get_all_mechanismen()

    if not mechanismen_liste:
        st.write("Keine Mechanismen vorhanden.")
        return
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        mechanismus_id = st.text_input("Name des neuen Mechanismus", key="mechanismus_id")

    with col2:
        st.markdown("<div style='text-align: center;'><br></div>", unsafe_allow_html=True)
        if st.button("Speichern"):
            if mechanismus_id:
                if mechanismus_id in qr.get_all_mechanismen():
                    st.warning(f"Ein Mechanismus mit der ID '{mechanismus_id}' existiert bereits!")
                else:
                    neuer_mechanismus = cl.Mechanismus(mechanismus_id)
                    qr.save_mechanismus(neuer_mechanismus, force=True)
                    st.session_state["aktueller_mechanismus"] = mechanismus_id
                    st.success(f"Mechanismus '{mechanismus_id}' gespeichert! Weiter zur Dateneingabe.")
                    st.rerun()

    with col3:
        selected_mechanismus_id = st.selectbox("Mechanismus auswählen", mechanismen_liste, index=0)
        if "aktueller_mechanismus" not in st.session_state or st.session_state["aktueller_mechanismus"] != selected_mechanismus_id:
            st.session_state["aktueller_mechanismus"] = selected_mechanismus_id
            if "punkte" in st.session_state:
                del st.session_state["punkte"]
            if "verbindungen" in st.session_state:
                del st.session_state["verbindungen"]
            st.rerun()


    with col4:
        st.markdown("<div style='text-align: center;'><br></div>", unsafe_allow_html=True)
        if st.button("Löschen"):
            qr.delete_mechanismus(selected_mechanismus_id)
            st.success(f"Mechanismus '{selected_mechanismus_id}' gelöscht!")
            st.rerun()

    st.divider()

    mechanismus = qr.load_mechanismus(st.session_state["aktueller_mechanismus"])
    if not mechanismus:
        st.error("Mechanismus konnte nicht geladen werden!")
        return

    col_links, col_rechts = st.columns([3, 3])

    with col_links:
        st.subheader("Punkte")

        if "punkte" not in st.session_state or not st.session_state["punkte"]:
            st.session_state["punkte"] = [(p.id, p.x, p.y, p.fix) for p in mechanismus.punkte.values()]

        col0, col1, col2, col3, col4 = st.columns([1, 2, 2, 2, 3])
        with col1:
            st.markdown("##### Punkt-ID")
        with col2:
            st.markdown("##### X")
        with col3:
            st.markdown("##### Y")
        with col4:
            st.markdown("##### Fixiert")

        neue_punkte = []
        for i, (name, x, y, fixiert) in enumerate(st.session_state["punkte"]):
            col0, col1, col2, col3, col4 = st.columns([1, 2, 2, 2, 2])

            with col0:
                st.markdown("<div style='text-align: center;'><br></div>", unsafe_allow_html=True)
                if st.button("X", key=f"delete_{i}"):
                    mechanismus.remove_point(name)
                    qr.save_mechanismus(mechanismus, force=True)
                    st.session_state["punkte"] = [(p.id, p.x, p.y, p.fix) for p in mechanismus.punkte.values()]
                    st.rerun()

            with col1:
                name = st.text_input(" ", value=name, key=f"name_{i}")

            with col2:
                x_koordinate = st.number_input(" ", value=x, step=0.1, key=f"x_{i}")

            with col3:
                y_koordinate = st.number_input(" ", value=y, step=0.1, key=f"y_{i}")

            with col4:
                st.markdown("<div style='text-align: center;'><br></div>", unsafe_allow_html=True)
                fixiert = st.checkbox(" ", value=fixiert, key=f"fix_{i}")

            neue_punkte.append((name, x_koordinate, y_koordinate, fixiert))

        st.session_state["punkte"] = neue_punkte
        
        st.write("")
        st.write("")
        col0, col1, col2, col4 = st.columns([2, 2, 2, 0.5])
        
        with col0:
            if st.button("Punkt hinzufügen"):
                st.session_state["punkte"].append((f"P{len(st.session_state['punkte']) + 1}", 0.0, 0.0, False))
                st.rerun()

        with col1:
            if st.button("Alle löschen"):
                st.session_state["punkte"] = []
                st.rerun()

        with col2:
            if st.button("Alle speichern"):
                mechanismus.punkte = {}
                for name, x, y, fixiert in st.session_state["punkte"]:
                    mechanismus.add_point(name, x, y, fixiert)
                
                qr.save_mechanismus(mechanismus)
                st.success("Punkte gespeichert!")

    with col_rechts:
        if "verbindungen" not in st.session_state:
            st.session_state["verbindungen"] = [(s.p1.id, s.p2.id) for s in mechanismus.stangen]
        
        st.subheader("Verbindungen")

        col0, col1, col2, col3 = st.columns([1, 3, 3, 2])
        with col1:
            st.markdown("##### Punkt 1")
        with col2:
            st.markdown("##### Punkt 2")
        
        for i, (p1, p2) in enumerate(st.session_state["verbindungen"]):
            col0, col1, col2, col3 = st.columns([1, 3, 3, 2])
            with col0:
                st.markdown("<div style='text-align: center;'><br></div>", unsafe_allow_html=True)
                if st.button("X", key=f"delete_conn_{i}"):
                    st.session_state["verbindungen"].pop(i)
                    mechanismus.remove_link(p1, p2)
                    qr.save_mechanismus(mechanismus, force=True)
                    st.rerun()
            with col1:
                punkte_ids = [p[0] for p in st.session_state["punkte"]]
                new_p1 = st.selectbox(" ", punkte_ids, index=punkte_ids.index(p1) if p1 in punkte_ids else 0, key=f"conn1_{i}")
            with col2:
                new_p2 = st.selectbox(" ", punkte_ids, index=punkte_ids.index(p2) if p2 in punkte_ids else 0, key=f"conn2_{i}")


        col0, col_new1, col_new2, col_action = st.columns([1, 3, 3, 2])
        
        with col_new1:
            new_p1 = st.selectbox(" ", [p[0] for p in st.session_state["punkte"]], key="new_punkt1")
            
        with col_new2:
            new_p2 = st.selectbox(" ", [p[0] for p in st.session_state["punkte"]], key="new_punkt2")
            
        with col_action:
            st.markdown("<div style='text-align: center;'><br></div>", unsafe_allow_html=True)
            if st.button("hinzufügen"):
                if new_p1 != new_p2:
                    neue_verbindung = (new_p1, new_p2)
                    if neue_verbindung not in st.session_state["verbindungen"] and (new_p2, new_p1) not in st.session_state["verbindungen"]:
                        st.session_state["verbindungen"].append(neue_verbindung)
                        mechanismus.add_link(new_p1, new_p2)
                        qr.save_mechanismus(mechanismus, force=True)
                        st.success("Verbindung hinzugefügt!")
                    else:
                        st.warning("Diese Verbindung existiert bereits!")
                else:
                    st.warning("Bitte unterschiedliche Punkte auswählen.")
                st.rerun()


    st.divider()

    st.subheader("Visualisierung")

    if not mechanismus.punkte:
        st.warning("Noch keine Punkte vorhanden.")
    else:
        placeholder = st.empty()
        visualisierung = cl.MechanismusVisualisierung(st.session_state["aktueller_mechanismus"])
        visualisierung.punkte = {p[0]: cl.Punkt(p[0], p[1], p[2], p[3]) for p in st.session_state["punkte"]}
        visualisierung.stangen = [cl.Stange(v[0] + "-" + v[1], visualisierung.punkte[v[0]], visualisierung.punkte[v[1]]) for v in st.session_state["verbindungen"]]
        visualisierung.plot(placeholder)
