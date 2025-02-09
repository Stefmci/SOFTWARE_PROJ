import streamlit as st
import mockup_ui as ui 

def main():
    st.sidebar.title("Navigation")
    
    if "Seite" not in st.session_state:
        st.session_state["Seite"] = "Startseite"

    option = st.sidebar.radio(
        "Wählen Sie eine Seite:", 
        ["Startseite", "Dateneingabe", "Simulation", "Analyse", "Optimierung", "Datenexport", "Erweiterungen"]
    )
    
    if option != st.session_state["Seite"]:
        st.session_state["Seite"] = option
        st.rerun()

    if st.session_state["Seite"] == "Startseite":
        ui.startseite()
    elif st.session_state["Seite"] == "Dateneingabe":
        ui.dateneingabe()
    elif st.session_state["Seite"] == "Simulation":
        ui.simulation()
    elif st.session_state["Seite"] == "Analyse":
        ui.analyse()
    elif st.session_state["Seite"] == "Optimierung":
        ui.optimierung()
    elif st.session_state["Seite"] == "Datenexport":
        ui.datenexportieren()
    elif st.session_state["Seite"] == "Erweiterungen":
        ui.erweiterungen()

if __name__ == "__main__":
    main()
