from entity import Entity
from math import sqrt
class Sheep(Entity):
    def __init__(self, canvas, x, y, alpha, beta, gamma, pr, pd, pg, safety = 5, r=10, color='blue'):
        super().__init__(canvas, x, y, r, color)
        self.safety = safety
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.pr = pr
        self.pd = pd
        self.pg = pg

    def psi(self, x):
        if x > self.pd:
            return 0
        elif x > self.pg:
            return self.gamma*(x-self.pg)
        elif x > self.pr:
            return 0
        elif x > self.ps:
            return self.beta*(1/(x-self.ps)-1/(self.pr-self.ps))
        raise Exception

    def phi(self, x):
        if x > self.pn:
            return 0
        elif x > 0:
            return self.alpha*(1/x-1/self.pn)
        raise Exception

    def vel_to_dog(self):
        x_to_dog = self.x - self.canvas.dog.x
        y_to_dog = self.y - self.canvas.dog.y
        ux_to_dog, uy_to_dog = self.unit(x_to_dog, y_to_dog)
        phi = self.phi(sqrt(x_to_dog**2+y_to_dog**2))
        return (phi*ux_to_dog, phi*uy_to_dog)

    def vel_to_sheeps(self):
        vel_x = 0
        vel_y = 0
        for sheep in self.canvas.sheeps:
            if sheep.id != self.id:
                x_to_sheep = self.x - sheep.x
                y_to_sheep = self.y - sheep.y
                ux_to_sheep, uy_to_sheep = self.unit(x_to_sheep, y_to_sheep)
                psi = self.psi(sqrt(x_to_sheep**2+y_to_sheep**2))
                vel_x += psi*ux_to_sheep
                vel_y += psi*uy_to_sheep
