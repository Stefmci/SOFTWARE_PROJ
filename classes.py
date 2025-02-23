import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import math
from typing import List

class Mechanism:
    def __init__(self, id=None):
        self.id = id
        self.points: List[Point] = []
        self.connections: List[Connection] = []

    def add_point(self, point: "Point"):
        self.points.append(point)

    def add_connection(self, point1_name, point2_name):
        p1 = next((p for p in self.points if p.id == point1_name or p.name == point1_name), None)
        p2 = next((p for p in self.points if p.id == point2_name or p.name == point2_name), None)
        if p1 and p2:
            connection = Connection(f"{point1_name}-{point2_name}", p1, p2)
            self.connections.append(connection)
        else:
            print(f"Fehler! Punkte '{point1_name}' und '{point2_name}' nicht gefunden!")

    def remove_point(self, name):
        self.points = [p for p in self.points if p.id != name and p.name != name]
        self.connections = [c for c in self.connections if c.point1.id != name and c.point2.id != name]

    def remove_connection(self, point1_name, point2_name):
        self.connections = [c for c in self.connections
                            if not ((c.point1.id == point1_name or c.point1.name == point1_name) and
                                    (c.point2.id == point2_name or c.point2.name == point2_name))]

    def move_point(self, name, x, y):
        point = next((p for p in self.points if p.id == name or p.name == name), None)
        if point:
            point.set_position(x, y)
        else:
            print(f"Punkt '{name}' nicht gefunden!")

    def relax_constraints(self, iterations=10):
        for _ in range(iterations):
            for v in self.connections:
                p1 = v.point1
                p2 = v.point2
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

    def erstelle_matrix(self):
        m = len(self.connections)
        n = len(self.points)
        A = np.zeros((2 * m, 2 * n))
        for i, v in enumerate(self.connections):
            p1_index = v.point1.id
            p2_index = v.point2.id
            A[2 * i, 2 * p1_index] = 1
            A[2 * i, 2 * p2_index] = -1
            A[2 * i + 1, 2 * p1_index + 1] = 1
            A[2 * i + 1, 2 * p2_index + 1] = -1
        return A

    def berechne_freiheitsgrad(self):
        n = len(self.points)
        m = len(self.connections)
        return 3 * (n - 1) - 2 * m

    def to_dict(self):
        return {
            "id": self.id,
            "points": [
                {
                    "id": p.id,
                    "name": p.name,
                    "x": p.x,
                    "y": p.y,
                    "fixed": p.fixed,
                    "color": p.color,
                    "trace_point": p.trace_point
                }
                for p in self.points
            ],
            "connections": [
                {"id": c.id, "point1": c.point1.id, "point2": c.point2.id, "length": c.length}
                for c in self.connections
            ]
        }


    @classmethod
    def from_dict(cls, data):
        mech = cls(data.get("id"))
        for p in data["points"]:
            point = Point(
                p["id"],
                p.get("name", p["id"]),
                p["x"],
                p["y"],
                p["fixed"],
                p.get("color", None),
                p.get("rot_point", None),
                p.get("rot_angle", 0),
                p.get("trace_point", False)
            )
            mech.add_point(point)
        for c in data["connections"]:
            mech.add_connection(c["point1"], c["point2"])
        return mech


class Point:
    def __init__(self, id: str, name: str, x: float, y: float, fixed: bool = False, color=None, rot_point: "Point" = None, rot_angle=0, trace_point=False):
        self.id = id
        self.name = name
        self.fixed = fixed
        self.trace_point = trace_point
        self.color = color if color is not None else ('blue' if fixed else 'red')
        if rot_point is not None:
            dx = x - rot_point.x
            dy = y - rot_point.y
            rad = math.radians(rot_angle)
            self.x = rot_point.x + dx * math.cos(rad) - dy * math.sin(rad)
            self.y = rot_point.y + dx * math.sin(rad) + dy * math.cos(rad)
        else:
            self.x = x
            self.y = y

    def get_position(self):
        return np.array([self.x, self.y])

    def set_position(self, x: float, y: float):
        if not self.fixed:
            self.x = x
            self.y = y

    def draw(self, ax, color=None):
        col = color if color is not None else self.color
        ax.scatter(self.x, self.y, color=col, s=50)
        ax.text(self.x + 0.5, self.y + 0.5, self.name, fontsize=12)

    def __str__(self):
        return f"Punkt(id={self.id}, name={self.name}, x={self.x}, y={self.y}, fixed={self.fixed})"

    def __repr__(self):
        return self.__str__()

class Connection:
    def __init__(self, id: str, point1: Point, point2: Point):
        self.id = id
        self.point1 = point1
        self.point2 = point2
        self.length = np.linalg.norm(self.point2.get_position() - self.point1.get_position())
        self.rest_length = self.distance()

    def get_endpoints(self):
        return self.point1.get_position(), self.point2.get_position()
    
    def distance(self):
        dx = self.point2.x - self.point1.x
        dy = self.point2.y - self.point1.y
        return math.sqrt(dx * dx + dy * dy)

    def draw(self, ax, color='blue'):
        ax.plot([self.point1.x, self.point2.x], [self.point1.y, self.point2.y], color=color)

    def __str__(self):
        return f"Verbindung(id={self.id}, length={self.length:.2f}, point1={self.point1.id}, point2={self.point2.id})"

    def __repr__(self):
        return self.__str__()

class MechanismVisualization(Mechanism):
    def __init__(self, id: str, pivot_id="P1", rotating_id="P2", trace_point_ids=None):
        super().__init__(id)
        self.fig, self.ax = plt.subplots(figsize=(8, 8))  # Größeres Fenster
        self.pivot_id = pivot_id
        self.rotating_id = rotating_id
        self.initial_positions = {}
        self.trace_point_ids = trace_point_ids if trace_point_ids else []  # Liste von Trace-Punkten
        self.trace_paths = {tp_id: [] for tp_id in self.trace_point_ids}  # Dictionary für mehrere Spuren


    def store_initial_positions(self):
        self.initial_positions = {}
        for point in self.points.values():
            if not point.fixed:
                self.initial_positions[point.id] = np.array([point.x, point.y])
        
        # Spuren für alle Trace-Punkte initialisieren
        self.trace_paths = {tp_id: [] for tp_id in self.trace_point_ids}
            
    def draw_trace(self, ax):
        """ Zeichnet die Spuren für alle gespeicherten Trace-Punkte """
        for tp_id, path in self.trace_paths.items():
            if path and len(path) > 1:
                x_vals, y_vals = zip(*path)
                ax.plot(x_vals, y_vals, color = "green", label=f"Trace {tp_id}")

    def plot(self, placeholder=None):
        self.ax.clear()
        self.ax.set_aspect('equal')
        self.ax.grid(True, linestyle='--', linewidth=0.5)
        
        # Punkte und Verbindungen plotten
        for point in self.points.values():
            point.draw(self.ax)
        for connection in self.connections:
            self.ax.plot([connection.point1.x, connection.point2.x],
                         [connection.point1.y, connection.point2.y],
                         color="blue")
        
        
        # Kreis um Punkt C
        center, point_A = None, None
        for point in self.points.values():
            if point.id == "c" or point.name == "c":
                center = point
            elif point.id == "A" or point.name == "A":
                point_A = point
        if center and point_A:
            radius = np.linalg.norm(np.array([point_A.x, point_A.y]) - np.array([center.x, center.y]))
            circle = plt.Circle((center.x, center.y), radius, color="red", fill=False)
            self.ax.add_patch(circle)
        
        self.draw_trace(self.ax)
        
        # Skalierung kleiner machen
        self.ax.set_xlim(-150, 150)
        self.ax.set_ylim(-150, 150)
        
        if placeholder:
            placeholder.pyplot(self.fig)
        else:
            st.pyplot(self.fig)

    def update(self, frame, placeholder):
        angle = np.radians(frame % 360)
        pivot = next((p for p in self.points if p.id == self.pivot_id), None)
        if not pivot:
            self.plot(placeholder)
            return

        rotating = next((p for p in self.points if p.id == self.rotating_id), None)
        if rotating and rotating.id in self.initial_positions:
            initial_vec = self.initial_positions[rotating.id] - np.array([pivot.x, pivot.y])
            new_vec = np.array([np.cos(angle), np.sin(angle)]) * np.linalg.norm(initial_vec)
            new_pos = np.array([pivot.x, pivot.y]) + new_vec
            rotating.set_position(new_pos[0], new_pos[1])

            # Spur für alle gespeicherten Trace-Punkte aktualisieren
            for tp_id in self.trace_point_ids:
                trace_point = next((p for p in self.points if p.id == tp_id), None)
                if trace_point:
                    self.trace_paths[tp_id].append((trace_point.x, trace_point.y))

        self.relax_constraints(1)
        self.plot(placeholder)
