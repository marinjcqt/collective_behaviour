from entity import Entity
class Sheepdog(Entity):
    def __init__(self, canvas, x, y, r=10, color='red'):
        super().__init__(canvas, x, y, r, color)

    def simulate(self, event):
        x_mouse, y_mouse = event.x, event.y
        self.moveto(x_mouse, y_mouse)
        # self.canvas.bind('<B1-Motion>', self.simulate)
        self.canvas.unbind('<B1-Motion>')
        self.canvas.after(100, lambda : self.canvas.bind('<B1-Motion>', self.simulate))