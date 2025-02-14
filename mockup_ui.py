import streamlit as st
import matplotlib.pyplot as plt
from mechanismus import Mechanism, create_mechanism  # Stelle sicher, dass Mechanism importiert ist
from plots import MechanismPlotter  # Falls MechanismPlotter in einer separaten Datei ist

def startseite():
    st.title("Simulation ebener Mechanismen")
    st.header("Abschlussprojekt - Softwaredesign")
    st.divider()
    st.write("Die Navigationsleiste leitet Sie durch die Simulation eines ebenen Mechanismus.") 
    st.divider()
    st.write("Um Eine Simulation zu starten, klicken Sie auf folgenden Button:") 
    if st.button("Start der Simulation"):
        st.success("Simulation gestartet!")
        st.session_state["Seite"] = "Dateneingabe"


def dateneingabe():
    st.title("Dateneingabe")
    st.write("Hier können Sie die benötigten Parameter für die Simulation eingeben.")
    st.divider()    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Punkt hinzufügen"):
            st.success("Punkt wurde hinzugefügt!")

    with col2:
        if st.button("Punkt löschen"):
            st.warning("Punkt wurde gelöscht!")

    with col3:
        if st.button("Punkte Reset"):
            st.error("Alle Punkte wurden zurückgesetzt!")
            
    with col4:
        if st.button("Simulation Reset"):
            st.success("Simulation abgebrochen!")
            st.session_state["Seite"] = "Startseite"
            
    st.divider()
            
    st.header("Punkte")
    param1 = st.number_input("Parameter 1", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
    param2 = st.slider("Parameter 2", min_value=0, max_value=360, value=180)
    st.write(f"Eingegebene Werte: Parameter 1 = {param1}, Parameter 2 = {param2}")
    
    if st.button("Weiter zur Simulation"):
        st.success("Weiter zur Simulation!")
        st.session_state["Seite"] = "Simulation"
        st.rerun()
    
def simulation():
    st.title("Simulation")
    st.write("Hier läuft die Simulation basierend auf den eingegebenen Parametern.")
    placeholder = st.empty()
    
    mechanism = create_mechanism()
    plotter = MechanismPlotter(mechanism)
    plotter.animate(placeholder)

def analyse():
    st.title("Analyse")
    st.header("MIN - Mech. verfizieren ob Valide")
    st.header("MIN - Test mittels Strandbeest")
    st.write("Eventuell Strandbeest in Datenbank speichern und bei Dokumentation beschreiben")
    st.divider()
    st.write("Hier werden die Ergebnisse der Simulation analysiert.")
    st.write("Ergebnisse der Simulation:")
    st.metric(label="Ergebnis 1", value="123.45", delta="5.67")

def optimierung():
    st.title("Optimierung")
    st.write("MIN - Kinematik als Optimierungsproblem gelöst")
    st.write("MIN - Optimierung der Simulation:")
    st.metric(label="Optimierung 1", value="123.45", delta="5.67")

def datenexportieren():
    st.title("Datenexport")
    st.write("Hier können Sie die Ergebnisse exportieren.")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("MIN - CSV (x(thetha), y(thetha))"):
            st.success("Punkt wurden gespeichert!")

    with col2:
        if st.button("MIN - Mechanismus speichern (Punkte?)"):
            st.warning("Punkt wurde gelöscht!")

    with col3:
        if st.button("Punkte Reset"):
            st.error("Alle Punkte wurden zurückgesetzt!")
            
    with col4:
        if st.button("Simulation Reset"):
            st.success("Simulation abgebrochen!")
            st.session_state = "Startseite"
            
    st.divider()
    st.header("MIN - Anwendung mit Streamlit deployed")

def erweiterungen():
    st.title("Erweiterungen")
    st.write("Hier können Sie die Simulation erweitern.")
    st.markdown("""
    ### Erweiterungen der Simulation:
    - **Visualisierung der Längen-Fehler** aller Glieder als Funktionen des Winkels \\( \\theta \\)
    - **Animation als Video/GIF speichern**
    - **Overlay** z. B. von Winkeln oder Längen auf die Visualisierung
    - **Lösen von Kinematiken**, bei denen ein Punkt noch einen Freiheitsgrad hat, z. B. eine Schubkurbel
    - **Definition einer Auszeichnungssprache**, um Modelle der Mechanismen zu beschreiben → Modell kann heruntergeladen und ggf. hochgeladen werden
    - **Optimieren der Gliederlängen** für eine bestimmte Bahnkurve bzw. eine Bahnkurve, die gewissen Kriterien entspricht
    """)



