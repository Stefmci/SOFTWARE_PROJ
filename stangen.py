import numpy as np
import matplotlib.pyplot as plt

class Stangen:
    def __init__(self, p1, p2, color='blue'):
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.length = np.linalg.norm(p2.position() - p1.position())

    def draw(self, ax):
        ax.plot([self.p1.x, self.p2.x], [self.p1.y, self.p2.y], color=self.color, linewidth=2)
