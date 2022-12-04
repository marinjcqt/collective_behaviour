import tkinter as tk
from tkinter.ttk import *
from sheep import Sheep
from sheepdog import Sheepdog
from enum import Enum

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

        
        
    def update_state(self, state):
        self.state = state
        if self.state == self.State.ADD_BARN:
            print("yes")
        elif self.state == self.State.ADD_SHEEPS:
            self.canvas.bind('<Button-1>', self.create_sheep)
        elif self.state == self.State.ADD_SHEEPDOG:
            self.canvas.bind('<Button-1>', self.create_sheepdog)
        elif self.state == self.State.SIMULATION:
            for entity in self.sheeps:
                entity.simulate()
            self.canvas.bind('<B1-Motion>', self.sheepdog.simulate)

    def create_sheep(self, event):
        print('sheep')
        x, y = event.x, event.y
        self.sheeps.append(Sheep(self, x, y, 200, 100, -1, 0.1, 0.1, 50, 15, 30, 2))

    
    def create_sheepdog(self, event):
        print('dog')
        x,y = event.x, event.y
        if self.sheepdog == None:
            self.sheepdog = Sheepdog(self, x,y)
        else:
            self.sheepdog.moveto(x, y)