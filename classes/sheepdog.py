from entity import Entity
class Sheepdog(Entity):
    def __init__(self, canvas, x, y, r=10, color='red'):
        super().__init__(canvas, x, y, r, color)