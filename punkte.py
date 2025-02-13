import numpy as np

class Punkte:
    def __init__(self, x: float, y: float):
        """Erstellt einen Punkt in der Ebene."""
        self.x = x
        self.y = y

    def get_position(self):
        """Gibt die Koordinaten des Punkts zurück."""
        return np.array([self.x, self.y])