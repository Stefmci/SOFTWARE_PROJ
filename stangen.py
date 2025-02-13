import numpy as np

class Stangen:
    def __init__(self, p1, p2):
        """Erstellt eine Stange zwischen zwei Punkten."""
        self.p1 = p1
        self.p2 = p2
        self.länge = np.linalg.norm(self.punkt2.get_position() - self.punkt1.get_position())

    def get_endpunkte(self):
        """Gibt die Koordinaten der Endpunkte der Stange zurück."""
        return self.punkt1.get_position(), self.punkt2.get_position()
