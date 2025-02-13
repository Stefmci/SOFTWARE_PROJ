import numpy as np

class Punkte:
    def __init__(self, x, y, fixed=False):
        self.x = x
        self.y = y
        self.fixed = fixed  # Speichert, ob der Punkt fixiert ist

    def position(self):
        return np.array([self.x, self.y])

    def move(self, x, y):
        if not self.fixed:  # Beweglich nur wenn nicht fixiert
            self.x = x
            self.y = y