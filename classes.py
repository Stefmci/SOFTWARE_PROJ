import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

class Mechanismus:
    def __init__(self, id: str):
        self.id = id
        self.punkte = {}
        self.stangen = []

    def add_point(self, name, x, y, fixed=False):
        self.punkte[name] = Punkt(name, x, y, fixed)

    def add_link(self, p1_name, p2_name):
        if p1_name in self.punkte and p2_name in self.punkte:
            stange = Stange(f"{p1_name}-{p2_name}", self.punkte[p1_name], self.punkte[p2_name])
            self.stangen.append(stange)

    def remove_point(self, name):
        if name in self.punkte:
            del self.punkte[name]

    def remove_link(self, p1_name, p2_name):
        self.stangen = [s for s in self.stangen if not (s.p1.id == p1_name and s.p2.id == p2_name)]

    def move_point(self, name, x, y):
        if name in self.punkte:
            self.punkte[name].set_position(x, y)
        else:
            print(f"Punkt '{name}' existiert nicht!")

    def to_dict(self):
        return {
            "id": self.id,
            "punkte": [{"id": p.id, "x": p.x, "y": p.y, "fixed": p.fix} for p in self.punkte.values()],
            "stangen": [{"id": s.id, "p1": s.p1.id, "p2": s.p2.id, "leange": s.leange} for s in self.stangen]
        }

    @classmethod
    def from_dict(cls, data):
        mechanismus = cls(data["id"])
        for p in data["punkte"]:
            mechanismus.add_point(p["id"], p["x"], p["y"], p["fixed"])
        for s in data["stangen"]:
            mechanismus.add_link(s["p1"], s["p2"])
        return mechanismus

class Punkt:
    def __init__(self, id: str, x: float, y: float, fix: bool = False):
        self.id = id
        self.x = x
        self.y = y
        self.fix = fix

    def get_position(self):
        return np.array([self.x, self.y])

    def set_position(self, x: float, y: float):
        if not self.fix:
            self.x = x
            self.y = y

    def __str__(self):
        return f"Punkt(id={self.id}, x={self.x}, y={self.y}, fix={self.fix})"

class Stange:
    def __init__(self, id: str, p1: Punkt, p2: Punkt):
        self.id = id
        self.p1 = p1
        self.p2 = p2
        self.leange = np.linalg.norm(self.p2.get_position() - self.p1.get_position())

    def get_endpunkte(self):
        return self.p1.get_position(), self.p2.get_position()

    def __str__(self):
        return f"Stange(id={self.id}, leange={self.leange:.2f}, p1={self.p1.id}, p2={self.p2.id})"

class MechanismusVisualisierung(Mechanismus):
    def __init__(self, id: str, pivot_id="P1", rotating_id="P2"):
        super().__init__(id)
        self.fig, self.ax = plt.subplots()
        self.pivot_id = pivot_id
        self.rotating_id = rotating_id
        self.initial_positions = {}

    def store_initial_positions(self):
        self.initial_positions = {}
        for pid, point in self.punkte.items():
            if not point.fix:
                self.initial_positions[pid] = np.array([point.x, point.y])

    def plot(self, placeholder=None):
        self.ax.clear()
        self.ax.set_xlim(-50, 50)
        self.ax.set_ylim(-20, 50)
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        for name, point in self.punkte.items():
            self.ax.scatter(point.x, point.y, color='red')
            self.ax.text(point.x + 0.5, point.y + 0.5, name, fontsize=12)
        for s in self.stangen:
            self.ax.plot([s.p1.x, s.p2.x], [s.p1.y, s.p2.y], color="blue")
        if placeholder:
            placeholder.pyplot(self.fig)
        else:
            st.pyplot(self.fig)

    def update(self, frame, placeholder):
        angle = np.radians(frame % 360)
        pivot = self.punkte.get(self.pivot_id)
        if pivot is None:
            self.plot(placeholder)
            return
        for pid, point in self.punkte.items():
            if not point.fix and pid in self.initial_positions:
                initial_vec = self.initial_positions[pid] - np.array([pivot.x, pivot.y])
                rot_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                       [np.sin(angle),  np.cos(angle)]])
                new_vec = rot_matrix.dot(initial_vec)
                new_pos = np.array([pivot.x, pivot.y]) + new_vec
                point.set_position(new_pos[0], new_pos[1])
        self.plot(placeholder)
        
