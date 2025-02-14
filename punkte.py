import numpy as np

class Punkte:
    def __init__(self, x: float, y: float, fix: bool = False):
        """Erstellt einen Punkt in der Ebene.
        
        Parameter:
        x, y -- Koordinaten des Punkts
        fix -- True, wenn der Punkt fixiert ist, sonst False
        """
        self.x = x
        self.y = y
        self.fix = fix

    def get_position(self):
        """Gibt die Koordinaten des Punkts zurück."""
        return np.array([self.x, self.y])

    def set_position(self, x: float, y: float):
        """Setzt die Koordinaten des Punkts (nur wenn nicht fixiert)."""
        if not self.fix:
            self.x = x
            self.y = y