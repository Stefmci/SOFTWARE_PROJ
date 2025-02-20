import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import List
import math

class Punkt:
    def __init__(self, id, name, x, y, fixed=False, farbe=None, rot_punkt=None, rot_angle=0):
        self.id = id
        self.name = name
        self.fixed = fixed
        self.farbe = farbe if farbe is not None else ('blue' if fixed else 'red')
        if rot_punkt is not None:
            dx = x - rot_punkt.x
            dy = y - rot_punkt.y
            rad = math.radians(rot_angle)
            self.x = rot_punkt.x + dx * math.cos(rad) - dy * math.sin(rad)
            self.y = rot_punkt.y + dx * math.sin(rad) + dy * math.cos(rad)
        else:
            self.x = x
            self.y = y

    def draw(self, ax, color=None):
        color = color if color is not None else self.farbe
        ax.scatter(self.x, self.y, color=color, s=50)
        ax.text(self.x + 0.5, self.y + 0.5, self.name, fontsize=12)

    def __repr__(self):
        return f"Punkt(id={self.id}, name={self.name}, x={self.x}, y={self.y}, fixed={self.fixed}, farbe={self.farbe})"

class Verbindung:
    def __init__(self, id, punkt1, punkt2):
        self.id = id
        self.punkt1 = punkt1
        self.punkt2 = punkt2
        self.rest_length = self.distance()

    def draw(self, ax, color='g'):
        ax.plot([self.punkt1.x, self.punkt2.x],
                [self.punkt1.y, self.punkt2.y],
                color + '-', linewidth=2)

    def distance(self):
        dx = self.punkt2.x - self.punkt1.x
        dy = self.punkt2.y - self.punkt1.y
        return math.sqrt(dx * dx + dy * dy)

    def __repr__(self):
        return f"Verbindung({self.punkt1.id} ↔ {self.punkt2.id})"

class Mechanismus:
    def __init__(self):
        self.punkte: List[Punkt] = []
        self.verbindungen: List[Verbindung] = []

    def punkt_hinzufuegen(self, punkt: Punkt):
        self.punkte.append(punkt)

    def verbindung_hinzufuegen(self, punkt1: Punkt, punkt2: Punkt):
        v = Verbindung(len(self.verbindungen), punkt1, punkt2)
        self.verbindungen.append(v)

    def erstelle_matrix(self):
        m = len(self.verbindungen)
        n = len(self.punkte)
        A = np.zeros((2 * m, 2 * n))
        for i, v in enumerate(self.verbindungen):
            p1_index = v.punkt1.id
            p2_index = v.punkt2.id
            A[2 * i, 2 * p1_index] = 1
            A[2 * i, 2 * p2_index] = -1
            A[2 * i + 1, 2 * p1_index + 1] = 1
            A[2 * i + 1, 2 * p2_index + 1] = -1
        return A

    def berechne_freiheitsgrad(self):
        n = len(self.punkte)
        m = len(self.verbindungen)
        return 3 * (n - 1) - 2 * m

    def berechne_laengen(self):
        laengen = []
        for v in self.verbindungen:
            dx = v.punkt2.x - v.punkt1.x
            dy = v.punkt2.y - v.punkt1.y
            laenge = math.sqrt(dx * dx + dy * dy)
            laengen.append(laenge)
            print("Länge Verbindung " + v.punkt1.name + " - " + v.punkt2.name + ": " + "{:.3f}".format(laenge))
        return laengen

    def zeichne_kreis_um_c(self, ax):
        point_c = next((p for p in self.punkte if p.name == "c"), None)
        point_A = next((p for p in self.punkte if p.name == "A"), None)
        if not point_c or not point_A:
            print("Punkt c oder A nicht gefunden!")
            return
        radius = math.hypot(point_A.x - point_c.x, point_A.y - point_c.y)
        circle = plt.Circle((point_c.x, point_c.y), radius, color='red', fill=False)
        ax.add_patch(circle)

    def relax_constraints(self, iterations=10):
        for _ in range(iterations):
            for v in self.verbindungen:
                p1 = v.punkt1
                p2 = v.punkt2
                dx = p2.x - p1.x
                dy = p2.y - p1.y
                d = math.sqrt(dx * dx + dy * dy)
                diff = d - v.rest_length
                nx = dx / d
                ny = dy / d
                factor = 0.8
                if (not p1.fixed and p1.name != "A") and (not p2.fixed and p2.name != "A"):
                    p1.x += factor * diff * nx
                    p1.y += factor * diff * ny
                    p2.x -= factor * diff * nx
                    p2.y -= factor * diff * ny
                elif not p1.fixed and p1.name != "A":
                    p1.x += diff * nx
                    p1.y += diff * ny
                elif not p2.fixed and p2.name != "A":
                    p2.x -= diff * nx
                    p2.y -= diff * ny

    def visualisiere(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        for v in self.verbindungen:
            v.draw(ax)
        for p in self.punkte:
            p.draw(ax)
        self.zeichne_kreis_um_c(ax)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Mechanismus Visualisierung")
        ax.grid(True)
        plt.show()

class Simulator:
    def __init__(self, mechanismus, frames=200, dt=0.05, figsize=(10,8), xlim=(-50,50), ylim=(-50,50)):
        self.mechanismus = mechanismus
        self.frames = frames
        self.dt = dt
        self.figsize = figsize
        self.xlim = xlim
        self.ylim = ylim

    def simulate(self):
        fig, ax = plt.subplots(figsize=self.figsize)
        ax.set_aspect('equal')
        ax.set_xlim(self.xlim)
        ax.set_ylim(self.ylim)
        point_c = next((p for p in self.mechanismus.punkte if p.name == "c"), None)
        point_A = next((p for p in self.mechanismus.punkte if p.name == "A"), None)
        if not point_c or not point_A:
            print("Punkt c oder A nicht gefunden!")
            return
        connection_c_A = next((v for v in self.mechanismus.verbindungen 
                               if (v.punkt1.name == "c" and v.punkt2.name == "A") or 
                                  (v.punkt1.name == "A" and v.punkt2.name == "c")), None)
        if connection_c_A is None:
            print("Verbindung c-A nicht gefunden!")
            return
        radius = connection_c_A.rest_length

        def update(frame):
            angle = frame * self.dt
            point_A.x = point_c.x + radius * math.cos(angle)
            point_A.y = point_c.y + radius * math.sin(angle)
            self.mechanismus.relax_constraints(10)
            ax.clear()
            ax.set_aspect('equal')
            ax.set_xlim(self.xlim)
            ax.set_ylim(self.ylim)
            for v in self.mechanismus.verbindungen:
                v.draw(ax)
            for p in self.mechanismus.punkte:
                p.draw(ax)
            self.mechanismus.zeichne_kreis_um_c(ax)
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_title("Mechanismus Simulation")
            ax.grid(True)

        ani = animation.FuncAnimation(fig, update, frames=self.frames, interval=50, repeat=True)
        plt.show()

if __name__ == "__main__":
    c = Punkt(0, "c", -30, 0, True, "red")
    A = Punkt(1, "A", -20, 10, False, "blue", c, 0)
    B = Punkt(2, "B", 0, 0, True, "blue")
    P1 = Punkt(3, "P1", 10, 40, False, "green")
    P2 = Punkt(4, "P2", 10, 20, False, "green")
    P3 = Punkt(5, "P3", -5, 15, False, "green")

    mech = Mechanismus()
    mech.punkt_hinzufuegen(c)
    mech.punkt_hinzufuegen(A)
    mech.punkt_hinzufuegen(B)
    mech.punkt_hinzufuegen(P1)
    mech.punkt_hinzufuegen(P2)
    mech.punkt_hinzufuegen(P3)

    mech.verbindung_hinzufuegen(c, A)
    mech.verbindung_hinzufuegen(A, P1)
    mech.verbindung_hinzufuegen(B, P1)
    mech.verbindung_hinzufuegen(B, P2)
    mech.verbindung_hinzufuegen(P1, P2)
    mech.verbindung_hinzufuegen(P1, P3)
    mech.verbindung_hinzufuegen(P3, B)

    fg = mech.berechne_freiheitsgrad()
    print(f"Freiheitsgrad: {fg}")
    mech.berechne_laengen()
    
    sim = Simulator(mech)
    sim.simulate()
