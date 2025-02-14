import numpy as np
from stangen import Stangen
from punkte import Punkte

class Mechanism:
    def __init__(self):
        self.punkte = {}  # Umbenannt für Konsistenz
        self.stangen = []

    def add_point(self, name, x, y, fixed=False):
        self.punkte[name] = Punkte(x, y, fixed)

    def add_link(self, p1_name, p2_name, color='blue'):
        self.stangen.append((self.punkte[p1_name], self.punkte[p2_name], color))

    def move_point(self, name, x, y):
        if name in self.punkte:  # Korrektur der Bedingung
            self.punkte[name].move(x, y)

    def update_mechanism(self, angle):
        c = self.punkte['c']
        p2 = self.punkte['p2']
        
        # p2 rotiert um c
        radius_p2 = np.sqrt((p2.x - c.x)**2 + (p2.y - c.y)**2)
        p2_x = c.x + radius_p2 * np.cos(np.radians(angle))
        p2_y = c.y + radius_p2 * np.sin(np.radians(angle))
        p2.move(p2_x, p2_y)

def create_mechanism():
    mechanism = Mechanism()
    mechanism.add_point('p0', 0, 0, fixed=True)
    mechanism.add_point('c', -30, 0, fixed=True)
    mechanism.add_point('p1', 10, 35)
    mechanism.add_point('p2', -25, 10)
    
    mechanism.add_link('p0', 'p1')
    mechanism.add_link('p1', 'p2')
    mechanism.add_link('c', 'p2', color='red')
    
    return mechanism
