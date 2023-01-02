from entity import Entity
from math import sqrt, pi, sin, cos
class Sheep(Entity):
    def __init__(self, canvas, x, y, alpha, beta, gamma, a, omega, pn, pr, pd, pg, safety = 5, r=10, color='blue'):
        super().__init__(canvas, x, y, r, color)
        self.safety = safety
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.a = a
        self.omega = omega
        self.pn = pn
        self.pr = pr
        self.pd = pd
        self.pg = pg
        self.step = 0
        self.ps = 10

    def psi(self, x):
        if x > self.pd:
            return 0
        elif x > self.pg:
            return self.gamma*(x-self.pg)
        elif x > self.pr:
            return 0
        elif x > self.ps:
            return self.beta*(1/(x-self.ps)-1/(self.pr-self.ps))
        else :
            return 0

    def phi(self, x):
        if x > self.pn:
            return 0
        elif x > 0:
            return self.alpha*(1/x-1/self.pn)
        raise Exception

    def vel_to_dog(self):
        x_to_dog = self.x - self.display.sheepdog.x
        y_to_dog = self.y - self.display.sheepdog.y
        ux_to_dog, uy_to_dog = self.unit(x_to_dog, y_to_dog)
        phi = self.phi(sqrt(x_to_dog**2+y_to_dog**2))
        return (phi*ux_to_dog, phi*uy_to_dog)

    def vel_to_sheeps(self):
        vel_x = 0
        vel_y = 0
        for sheep in self.display.sheeps:
            if sheep.id != self.id:
                x_to_sheep = self.x - sheep.x
                y_to_sheep = self.y - sheep.y
                ux_to_sheep, uy_to_sheep = self.unit(x_to_sheep, y_to_sheep)
                psi = self.psi(sqrt(x_to_sheep**2+y_to_sheep**2))
                vel_x += psi*ux_to_sheep
                vel_y += psi*uy_to_sheep
        return (vel_x, vel_y)

    def velocity(self):
        vel_to_sheeps_x, vel_to_sheeps_y = self.vel_to_sheeps()
        vel_to_dog_x, vel_to_dog_y = self.vel_to_dog()
        angle = self.a*pi/180*sin(self.omega*self.step*self.sampling)
        x_rot = (cos(angle), -sin(angle))
        y_rot = (sin(angle), cos(angle))

        self.x_vel = vel_to_dog_x + x_rot[0]*vel_to_sheeps_x + x_rot[1]*vel_to_sheeps_y
        self.alphay_vel = vel_to_dog_y + y_rot[0]*vel_to_sheeps_x + y_rot[1]*vel_to_sheeps_y

    def is_visible(self):
        # Fist, check if the dog can see the sheep 
        if sqrt((self.x - self.display.sheepdog.x)**2 + (self.y - self.display.sheepdog.y)**2) > self.display.sheepdog.vision:
            self.visible = False
            return
        for sheep in self.display.sheeps:
            if sheep.id != self.id:
                # Check if the sheep is visible by the dog
                if self.unit(self.x - self.display.sheepdog.x, self.y - self.display.sheepdog.y) == self.unit(sheep.x - self.display.sheepdog.x, sheep.y - self.display.sheepdog.y) and sqrt((self.x - self.display.sheepdog.x)**2 + (self.y - self.display.sheepdog.y)**2) > sqrt((sheep.x - self.display.sheepdog.x)**2 + (sheep.y - self.display.sheepdog.y)**2):
                    self.visible = False
                    return
        self.visible = True

    def change_color(self):
        if self.visible:
            self.canvas.itemconfig(self.id, fill='green')
        else:
            self.canvas.itemconfig(self.id, fill='blue')
    def simulate(self):
        # Compute the new position
        self.velocity()
        self.move(self.sampling*self.x_vel, self.sampling*self.y_vel)

        # Check if the sheep is visible
        self.is_visible()
        self.change_color()

        self.canvas.after(100, self.simulate)