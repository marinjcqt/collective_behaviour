import tkinter as tk
from tkinter.ttk import *
from sheep import Sheep
from sheepdog import Sheepdog
from barn import Barn
from enum import Enum
import math

safety = 5
gain_to_dog = 7000
gain_to_sheep_low = 1400
gain_to_sheep_high = -140
angle_gain = 0.1
angle_param = 0.1
dist_low = 15
dist_high = 30
dist_mid = 20

vision = 50
angle_threshold = 2*math.pi/3
rot_left = -math.pi/4 % (2*math.pi)
rot_right = math.pi/4
radius_threshold = 40
inradius_gain = -450
outradius_gain = -375

sampling = 0.005

class Display:
    class State(Enum):
        ADD_SHEEPS = 0
        ADD_SHEEPDOG = 1
        ADD_BARN = 2
        SIMULATION = 3



    def __init__(self, width, height):
        self.window = tk.Tk()
        self.window.geometry(f"{width}x{height}")

        self.canvas = tk.Canvas(self.window, height=height, width=width)
        self.canvas.place(x=0, y=0)

        self.top_frame = tk.Frame(self.window, height=105, width=100)
        self.top_frame.grid(row=0, column=0)
        self.top_frame.tkraise()
        self.top_frame.pack_propagate(False)
        self.sheeps_button = Button(self.top_frame, text="Add Sheeps", command=lambda: self.update_state(self.State.ADD_SHEEPS))
        self.sheeps_button.pack()
        self.sheeps_button.focus()
        self.sheepdog_button = Button(self.top_frame, text="Add Sheepdog", command=lambda: self.update_state(self.State.ADD_SHEEPDOG))
        self.sheepdog_button.pack()
        self.barn_button = Button(self.top_frame, text="Add Barn", command=lambda: self.update_state(self.State.ADD_BARN))
        self.barn_button.pack()
        self.run_sim = Button(self.top_frame, text="Run Simulation", command=lambda: self.update_state(self.State.SIMULATION))
        self.run_sim.pack()
        self.state=None

        self.sheeps = []
        self.sheepdog = None

        self.barn_radius = 100
        
    def update_state(self, state):
        self.state = state
        if self.state == self.State.ADD_BARN:
            self.canvas.bind('<Button-1>', self.create_barn)
        elif self.state == self.State.ADD_SHEEPS:
            self.canvas.bind('<Button-1>', self.create_sheep)
        elif self.state == self.State.ADD_SHEEPDOG:
            self.canvas.bind('<Button-1>', self.create_sheepdog)
        elif self.state == self.State.SIMULATION:
            self.canvas.unbind('<Button-1>')
            for entity in self.sheeps + [self.sheepdog]:
                print(entity.id)
                entity.simulate()

    def create_sheep(self, event):
        x, y = event.x, event.y
        self.sheeps.append(Sheep(self, x, y, gain_to_dog, gain_to_sheep_low, gain_to_sheep_high, angle_gain, angle_param, dist_low, dist_high, dist_mid, safety, sampling))

    
    def create_sheepdog(self, event):
        x,y = event.x, event.y
        if self.sheepdog == None:
            self.sheepdog = Sheepdog(self, x,y, vision, angle_threshold, radius_threshold, rot_left, rot_right, inradius_gain, outradius_gain, sampling)
        else:
            self.sheepdog.moveto(x, y)

    def create_barn(self, event):
        x, y = event.x, event.y
        self.barn = Barn(self, x, y, self.barn_radius)

