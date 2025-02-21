import streamlit as st
import classes as cl
import queries as qr

def mechanismus_verwaltung():
    
########################################################## Überschrift

    st.subheader("Mechanism Management")
    st.divider()
    
########################################################## Mechanismen-Verwaltung

    mechanism_list = qr.get_all_mechanisms()

    if not mechanism_list:
        st.write("Kein Mechanismus vorhanden.")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        mechanism_id = st.text_input("Name des neuen Mechanismus", key="mechanism_id")

    with col2:
        st.markdown("<div style='text-align: center;'><br></div>", unsafe_allow_html=True)
        if st.button("Speichern"):
            if mechanism_id:
                if mechanism_id in qr.get_all_mechanisms():
                    st.warning(f"Existiert bereits!")
                else:
                    new_mechanism = cl.Mechanism(mechanism_id)
                    point_c = cl.Point("c", "c", -30, 0, True, "blue")
                    point_A = cl.Point("A", "A", -20, 10, False, "blue")
                    connection = cl.Connection("c-A", point_c, point_A)
                    new_mechanism.add_point(point_c)
                    new_mechanism.add_point(point_A)
                    qr.save_mechanism(new_mechanism, force=True)
                    st.session_state["current_mechanism"] = mechanism_id
                    st.success(f"'{mechanism_id}' wurde angelegt!")
                    st.rerun()

    with col3:
        selected_mechanism_id = st.selectbox("Bestehnden Wählen", mechanism_list, index=0)
        if ("current_mechanism" not in st.session_state or 
            st.session_state["current_mechanism"] != selected_mechanism_id):
            st.session_state["current_mechanism"] = selected_mechanism_id
            if "points" in st.session_state:
                del st.session_state["points"]
            if "connections" in st.session_state:
                del st.session_state["connections"]
            st.rerun()

    with col4:
        st.markdown("<div style='text-align: center;'><br></div>", unsafe_allow_html=True)
        if st.button("Löschen"):
            qr.delete_mechanism(selected_mechanism_id)
            st.success(f"'{selected_mechanism_id}' wurde gelöscht!")
            st.rerun()
            

    st.divider()

    mechanism = qr.load_mechanism(st.session_state["current_mechanism"])
    if not mechanism:
        st.success("Kein Mechanismus ausgewählt.")
        return

########################################################## Spalte links und rechts

    col_left, col_right = st.columns([4, 3])
    
########################################################## Punkte

    with col_left:
        st.write("##### Punkte")

        if "points" not in st.session_state or not st.session_state["points"]:
            st.session_state["points"] = [(p.id, p.x, p.y, p.fixed) for p in mechanism.points]

        col0, col1, col2, col3, col4 = st.columns([1, 2, 2, 2, 3])
        with col1:
            st.markdown("Point ID")
        with col2:
            st.markdown("X")
        with col3:
            st.markdown("Y")
        with col4:
            st.markdown("Fixed")

        new_points = []
        
        for i, (point_id, x, y, fixed) in enumerate(st.session_state["points"]):
            
            col0, col1, col2, col3, col4 = st.columns([1, 2, 2, 2, 2])
            
            with col0:
                st.markdown("<div style='text-align: center;'><br></div>", unsafe_allow_html=True)
                if point_id not in ("c", "A"):
                    if st.button("X", key=f"delete_{i}"):
                        mechanism.remove_point(point_id)
                        qr.save_mechanism(mechanism, force=True)
                        st.session_state["points"].pop(i)
                        st.rerun()
                        
            with col1:

                if point_id in ("c", "A"):
                    st.text_input(" ", value=point_id, key=f"name_{i}", disabled=True)
                else:
                    point_id = st.text_input(" ", value=point_id, key=f"name_{i}")
                
            with col2:
                x_coordinate = st.number_input(" ", value=float(x), step=0.1, key=f"x_{i}")
                
            with col3:
                y_coordinate = st.number_input(" ", value=float(y), step=0.1, key=f"y_{i}")
                
            with col4:
                st.markdown("<div style='text-align: center;'><br></div>", unsafe_allow_html=True)
                if point_id == "A":
                    st.write("")
                elif point_id.lower() == "c":
                    st.checkbox(" ", value=True, key=f"fix_{i}", disabled=True)
                else:
                    fixed = st.checkbox(" ", value=fixed, key=f"fix_{i}")
                            
            new_points.append((point_id, x_coordinate, y_coordinate, fixed))
            
        st.session_state["points"] = new_points
        
    

########################################################## Verbindungen

    with col_right:
        if "connections" not in st.session_state:
            st.session_state["connections"] = [(c.point1.id, c.point2.id) for c in mechanism.connections]
        st.write("##### Verbindungen")

        col0, col1, col2, col3 = st.columns([1, 3, 3, 2])
        
        with col1:
            st.markdown("Punkt 1")
            
        with col2:
            st.markdown("Punkt 2")
            
        for i, (p1, p2) in enumerate(st.session_state["connections"]):
            col0, col1, col2 = st.columns([1, 3, 3])
            fixed_connection = ((p1 == "c" and p2 == "A") or (p1 == "A" and p2 == "c"))
            
            with col0:
                st.markdown("<div style='text-align: center;'><br></div>", unsafe_allow_html=True)
                if not fixed_connection:
                    if st.button("X", key=f"delete_conn_{i}"):
                        st.session_state["connections"].pop(i)
                        mechanism.remove_connection(p1, p2)
                        qr.save_mechanism(mechanism, force=True)
                else:
                    st.write("")

            with col1:
                connection_ids = [p[0] for p in st.session_state["points"]]
                new_p1 = st.selectbox(
                    " ", 
                    connection_ids, 
                    index=connection_ids.index(p1) if p1 in connection_ids else 0, 
                    key=f"conn1_{i}",
                    disabled=fixed_connection
                )
            with col2:
                new_p2 = st.selectbox(
                    " ", 
                    connection_ids, 
                    index=connection_ids.index(p2) if p2 in connection_ids else 0, 
                    key=f"conn2_{i}",
                    disabled=fixed_connection
                )

        col0, col_new1, col_new2 = st.columns([1, 3, 3])
        with col_new1:
            new_p1 = st.selectbox(" ", [p[0] for p in st.session_state["points"]], key="new_point1")
        with col_new2:
            new_p2 = st.selectbox(" ", [p[0] for p in st.session_state["points"]], key="new_point2")


########################################################## Steuerung


    if selected_mechanism_id != "Keine Mechanismen vorhanden":
        loaded_mech = qr.load_mechanism(selected_mechanism_id)
        points_list = loaded_mech.points
    else:
        loaded_mech = None
        points_list = []
                    
    st.divider()

    col0, col1, col2, col3, col4 = st.columns([2, 2, 2, 2, 2])
    with col0:
        if st.button("Punkt hinzufügen"):
            st.session_state["points"].append((f"P{len(st.session_state['points']) + 1}", 0.0, 0.0, False))
            st.rerun()
            
    with col1:
        if st.button("Verbindung hinzufügen"):
            if new_p1 != new_p2:
                new_connection = (new_p1, new_p2)
                if (new_connection not in st.session_state["connections"] and
                    (new_p2, new_p1) not in st.session_state["connections"]):
                    st.session_state["connections"].append(new_connection)
                    mechanism.add_connection(new_p1, new_p2)
                    qr.save_mechanism(mechanism, force=True)
                    st.success("Connection added!")
                else:
                    st.warning("This connection already exists!")
            else:
                st.warning("Please choose different points.")
            st.rerun()
        
    with col2:
        if st.button("Alles Löschen"):
            st.session_state["points"] = []
            st.session_state["connections"] = []
            st.rerun()
            
    with col3:
        if st.button("Alles Speichern"):
            mechanism.points = []
            for point_id, x, y, fixed in st.session_state["points"]:
                new_point = cl.Point(point_id, point_id, x, y, fixed)
                mechanism.add_point(new_point)
            mechanism.connections = []
            for p1, p2 in st.session_state["connections"]:
                mechanism.add_connection(p1, p2)
            qr.save_mechanism(mechanism, force=True)
            st.success("saved!")
            
    with col4:
        if points_list:
            selected_point = st.selectbox("Wähle einen Punkt für die Bahnkurve", [p.name for p in mechanism.points])
        if st.button("Trace-Punkt setzen"):
            qr.save_trace(mechanism_id=mechanism.id, point_id=selected_point)
            st.success(f"Trace-Punkt für '{selected_point}' gesetzt.")

########################################################## Visualisierung

    st.divider()

    st.subheader("Visualization")
    if not mechanism.points:
        st.warning("No points available yet.")
    else:
        placeholder = st.empty()
        visualization = cl.MechanismVisualization(st.session_state["current_mechanism"])
        visualization.points = {p[0]: cl.Point(p[0], p[0], p[1], p[2], p[3]) for p in st.session_state["points"]}
        visualization.connections = [
            cl.Connection(f"{v[0]}-{v[1]}", visualization.points[v[0]], visualization.points[v[1]])
            for v in st.session_state["connections"]
        ]
        visualization.plot(placeholder)
