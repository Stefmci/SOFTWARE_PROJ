import streamlit as st
import classes as cl
import matplotlib.pyplot as plt
import numpy as np
import classes as cl

            
def erweiterungen():
    st.title("Erweiterungen")
    
    st.divider()
    st.markdown("""
    ### Erweiterungen der Simulation:
    - **Visualisierung der Längen-Fehler** als Funktionen des Winkels \\( \\theta \\)
    - **Animation als Video/GIF speichern**
    - **Overlay von Winkeln oder Längen auf die Visualisierung**
    - **Lösen von Kinematiken mit zusätzlichen Freiheitsgraden**
    - **Definition einer Auszeichnungssprache für Mechanismus-Modelle**
    - **Optimieren der Gliederlängen für eine bestimmte Bahnkurve**
    - **Alternative UI-Ansätze z. B. Drag & Drop oder Sketches**
    - **Import von Sketches mit Bilderkennung**
    - **Erstellen einer Stückliste für Mechanismus-Komponenten**
    - **Maximale Vorwärts-Geschwindigkeit eines Mechanismus berechnen**
    - **3D-Volumenmodell mit OpenSCAD erstellen**
    - **Erweiterung um Kräfte/Momente für Kinetik-Simulation**
    """)
