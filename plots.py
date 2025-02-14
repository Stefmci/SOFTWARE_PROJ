import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.animation import FuncAnimation
from punkte import Punkte
from stangen import Stangen
from mechanismus import Mechanism, create_mechanism

class MechanismPlotter:
    def __init__(self, mechanism):
        self.mechanism = mechanism
        self.fig, self.ax = plt.subplots()
        self.ani = None

    def plot(self, placeholder=None):
        self.ax.clear()
        self.ax.set_xlim(-50, 50)
        self.ax.set_ylim(-20, 50)
        self.ax.set_aspect('equal')
        self.ax.grid(True)

        # Punkte zeichnen
        for name, point in self.mechanism.punkte.items():
            self.ax.scatter(point.x, point.y, color='red')
            self.ax.text(point.x + 0.5, point.y + 0.5, name, fontsize=12)

        # Stangen zeichnen
        for p1, p2, color in self.mechanism.stangen:
            self.ax.plot([p1.x, p2.x], [p1.y, p2.y], color=color)

        if placeholder:
            placeholder.pyplot(self.fig)
        else:
            st.pyplot(self.fig)

    def update(self, frame, placeholder):
        angle = frame % 360  # Winkel von 0 bis 360 Grad
        self.mechanism.update_mechanism(angle)
        self.plot(placeholder)

    def animate(self, placeholder):
        self.ani = FuncAnimation(self.fig, self.update, frames=range(0, 360, 2), fargs=(placeholder,), interval=50, repeat=True)
        self.plot(placeholder)