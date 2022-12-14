from random import randint
from math import sqrt
import numpy as np
class Entity:
    def __init__(self, display, x, y, r=5, color='black'):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.display = display
        self.canvas = display.canvas
        self.id = self.canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill=self.color, outline=self.color)
        self.sampling = 10
        self.x_vel = 0
        self.y_vel = 0

    def moveto(self, x, y):
        """Moves the entity to the point (x, y)"""
        self.x = x
        self.y = y
        self.canvas.moveto(self.id, self.x - self.r, self.y - self.r)

    def move(self, x_vel, y_vel):
        """Moves the entity by (x_vel, y_vel)"""
        self.x += x_vel
        self.y += y_vel
        self.canvas.move(self.id, x_vel, y_vel)

    def simulate(self):
        """Simulates the entity's movement as a random walk"""
        x_vel = randint(-self.max_vel, self.max_vel)
        y_vel = randint(-self.max_vel, self.max_vel)
        self._sim(x_vel, y_vel)


    def _sim(self, x_vel, y_vel):
        """Simulates the entity's movement as a random walk (subroutine)"""
        self.move(self.sampling*x_vel, self.sampling*y_vel)
        self.canvas.after(10, lambda: self._sim(x_vel, y_vel))

    def unit(self, x, y):
        """Returns the unit vector of the vector (x, y)"""
        if x == 0 and y == 0:
            return np.array([0, 0])
        return np.array([x, y])/np.linalg.norm(np.array([x, y]))

    def distance(self, x, y):
        """Returns the distance between the entity and the point (x, y)"""
        return sqrt((self.x-x)**2+(self.y-y)**2)

