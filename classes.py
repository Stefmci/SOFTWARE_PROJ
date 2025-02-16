import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.animation import FuncAnimation
from tinydb import TinyDB, Query
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')
db = TinyDB(db_path)

class mechanismus:
    def __init__(self, id: str):
        self.id = id
        self.punkte = {}
        self.stangen = []

    def add_point(self, name, x, y, fixed=False):
        self.punkte[name] = Punkte(name, x, y, fixed)

    def add_link(self, p1_name, p2_name):
        if p1_name in self.punkte and p2_name in self.punkte:
            stange = Stangen(f"{p1_name}-{p2_name}", self.punkte[p1_name], self.punkte[p2_name])
            self.stangen.append(stange)

    def move_point(self, name, x, y):
        if name in self.punkte:
            self.punkte[name].set_position(x, y)

    def to_dict(self):
        return {
            "id": self.id,
            "punkte": [vars(p) for p in self.punkte.values()],
            "stangen": [{"id": s.id, "p1": s.p1.id, "p2": s.p2.id, "länge": s.länge} for s in self.stangen]
        }

    @classmethod
    def from_dict(cls, data):
        mechanismus = cls(data["id"])
        for p in data["punkte"]:
            mechanismus.add_point(p["id"], p["x"], p["y"], p["fix"])
        for s in data["stangen"]:
            mechanismus.add_link(s["p1"], s["p2"])
        return mechanismus

class Punkte(mechanismus):
    def __init__(self, id: str, x: float, y: float, fix: bool = False):
        super().__init__(id)
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
        return f"Punkte(id={self.id}, x={self.x}, y={self.y}, fix={self.fix})"

class Stangen(mechanismus):
    def __init__(self, id: str, p1: Punkte, p2: Punkte):
        super().__init__(id)
        self.p1 = p1
        self.p2 = p2

        self.länge = np.linalg.norm(self.p2.get_position() - self.p1.get_position())

    def get_endpunkte(self):
        return self.p1.get_position(), self.p2.get_position()

    def __str__(self):
        return f"Stangen(id={self.id}, Länge={self.länge:.2f}, p1={self.p1.id}, p2={self.p2.id})"

class MechanismusVisualisierung(mechanismus):
    def __init__(self, id: str):
        super().__init__(id)
        self.fig, self.ax = plt.subplots()
        self.ani = None

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
        angle = frame % 360
        self.move_point("B", np.cos(np.radians(angle)) * 10, np.sin(np.radians(angle)) * 10)
        self.plot(placeholder)

    def animate(self, placeholder):
        self.ani = FuncAnimation(self.fig, self.update, frames=range(0, 360, 2), fargs=(placeholder,), interval=50, repeat=True)
        self.plot(placeholder)


def save_mechanismus(mechanismus: mechanismus, force=False):
    mechanisms_table = db.table("mechanisms")
    query = Query()

    existing = mechanisms_table.get(query.id == mechanismus.id)
    
    if existing and not force:
        print(f"Mechanismus mit ID '{mechanismus.id}' existiert bereits! Nutze `force=True`, um ihn zu überschreiben.")
        return

    mechanisms_table.upsert(mechanismus.to_dict(), query.id == mechanismus.id)
    print(f"Mechanismus '{mechanismus.id}' wurde gespeichert {'(Überschrieben)' if existing else '(Neu)'}!")


def load_mechanismus(id: str) -> mechanismus:
    mechanisms_table = db.table("mechanisms")
    query = Query()
    result = mechanisms_table.get(query.id == id)
    
    if result:
        return mechanismus.from_dict(result)
    else:
        print(f"mechanismus mit ID '{id}' nicht gefunden.")
        return None

def get_all_mechanismen():
    mechanisms_table = db.table("mechanisms")
    return [m["id"] for m in mechanisms_table.all()]

def delete_mechanismus(id: str):
    mechanisms_table = db.table("mechanisms")
    query = Query()
    mechanisms_table.remove(query.id == id)
    print(f"mechanismus mit ID '{id}' wurde gelöscht.")

def update_mechanismus(id: str, neue_punkte=None, neue_stangen=None):
    mechanismus = load_mechanismus(id)
    if not mechanismus:
        print(f"mechanismus mit ID '{id}' nicht gefunden.")
        return
    
    if neue_punkte:
        for p in neue_punkte:
            mechanismus.add_point(p["id"], p["x"], p["y"], p["fix"])
    
    if neue_stangen:
        for s in neue_stangen:
            mechanismus.add_link(s["p1"], s["p2"])

    save_mechanismus(mechanismus)
    print(f"mechanismus '{id}' wurde aktualisiert.")