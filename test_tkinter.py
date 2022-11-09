import tkinter as tk
import random
from math import sin


def move(obj, func):
    x, y, _, _ = canvas.coords(obj)
    vx,vy = func(x,y)
    canvas.move(obj, vx, vy)
    window.after(10, move, obj, func)

w  = 25
h = 25

v = 1

window = tk.Tk()
window.geometry("1000x1000")

canvas = tk.Canvas(window, height=1000, width=1000)
canvas.grid(row=0, column=0, sticky='w')

circle1 = canvas.create_oval([0, 200, 0+w, 200+h], outline="red", fill="red")
circle2 = canvas.create_oval([500, 500, 500+w, 500+h], outline="blue", fill="blue")

window.after(0, move, circle1, lambda x,y: (v, 10*sin(x/(20*v))))
window.after(0, move, circle1, move(circle2, lambda x,y: (v, -v)))
window.mainloop()