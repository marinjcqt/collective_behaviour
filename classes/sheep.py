from entity import Entity
class Sheep(Entity):
    def __init__(self, canvas, x, y, r=10, color='blue'):
        super().__init__(canvas, x, y, r, color)
