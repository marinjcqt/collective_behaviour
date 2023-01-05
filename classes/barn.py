class Barn:
    def __init__(self, display, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.display = display
        self.canvas = display.canvas
        self.draw()

    def draw(self):
        """Draws the barn on the canvas"""
        self.canvas.create_oval(self.x - 5, self.y - 5, self.x + 5, self.y + 5, fill="orange", outline="orange")
        self.canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius, outline = "orange")

    def is_inside(self, x, y):
        """Returns True if the point (x, y) is inside the barn"""
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.radius ** 2

    def moveto(self, x, y):
        """Moves the barn to the point (x, y)"""
        self.x = x
        self.y = y
        self.canvas.moveto(self.id, self.x - self.r, self.y - self.r)

    def __str__(self):
        return f"Barn at ({self.x}, {self.y}), radius {self.radius}"

    def __repr__(self):
        return self.__str__()