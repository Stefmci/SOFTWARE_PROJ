import numpy as np

class Stangen:
    def __init__(self, p1, p2):
        """Erstellt eine Stange zwischen zwei Punkten."""
        self.p1 = p1  # Startpunkt (Objekt vom Typ Punkt)
        self.p2 = p2  # Endpunkt (Objekt vom Typ Punkt)

        # Berechnung der Länge anhand der Koordinaten
        self.länge = np.linalg.norm(np.array(self.p2.get_position()) - np.array(self.p1.get_position()))

    def get_endpunkte(self):
        """Gibt die Koordinaten der Endpunkte der Stange zurück."""
        return self.p1.get_position(), self.p2.get_position()
