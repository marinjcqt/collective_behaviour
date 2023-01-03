from entity import Entity
from math import sqrt, pi, sin, cos
import numpy as np 

class Sheep(Entity):
    def __init__(self, canvas, x, y, gain_to_dog, gain_to_sheep_low, gain_to_sheep_high, angle_gain, angle_param, dist_low, dist_high, dist_mid, safety, sampling, r=5, color='blue'):
        super().__init__(canvas, x, y, r, color)
        self.safety = safety
        self.gain_to_dog = gain_to_dog
        self.gain_to_sheep_low = gain_to_sheep_low
        self.gain_to_sheep_high = gain_to_sheep_high
        self.angle_gain = angle_gain
        self.angle_param = angle_param
        self.dist_low = dist_low
        self.dist_high = dist_high
        self.dist_mid = dist_mid
        self.sampling = sampling
        self.step = 0

    def reaction_to_sheeps(self, x):
        if x > self.dist_high:
            return 0
        elif x > self.dist_mid:
            return self.gain_to_sheep_high*(x-self.dist_mid)
        elif x > self.dist_low:
            return 0
        elif x > self.safety:
            return self.gain_to_sheep_low*(1/(x-self.safety)-1/(self.dist_low-self.safety))
        else :
            return 0

    def reaction_to_dog(self, x):
        dog_vision = self.display.sheepdog.vision
        if x > dog_vision:
            return 0
        elif x > 0:
            return self.gain_to_dog*(1/x-1/dog_vision)
        raise Exception

    def vel_to_dog(self):
        x_to_dog = self.x - self.display.sheepdog.x
        y_to_dog = self.y - self.display.sheepdog.y
        ux_to_dog, uy_to_dog = self.unit(x_to_dog, y_to_dog)
        reaction_to_dog = self.reaction_to_dog(sqrt(x_to_dog**2+y_to_dog**2))
        return (reaction_to_dog*ux_to_dog, reaction_to_dog*uy_to_dog)

    def vel_to_sheeps(self):
        vel_x = 0
        vel_y = 0
        for sheep in self.display.sheeps:
            if sheep.id != self.id:
                x_to_sheep = self.x - sheep.x
                y_to_sheep = self.y - sheep.y
                ux_to_sheep, uy_to_sheep = self.unit(x_to_sheep, y_to_sheep)
                reaction_to_sheeps = self.reaction_to_sheeps(sqrt(x_to_sheep**2+y_to_sheep**2))
                vel_x += reaction_to_sheeps*ux_to_sheep
                vel_y += reaction_to_sheeps*uy_to_sheep
        return (vel_x, vel_y)

    def velocity(self):
        vel_to_sheeps_x, vel_to_sheeps_y = self.vel_to_sheeps()
        vel_to_dog_x, vel_to_dog_y = self.vel_to_dog()
        angle = self.angle_gain*pi/180*sin(self.angle_param*self.step*self.sampling)
        x_rot = (cos(angle), -sin(angle))
        y_rot = (sin(angle), cos(angle))

        self.x_vel = vel_to_dog_x + x_rot[0]*vel_to_sheeps_x + x_rot[1]*vel_to_sheeps_y
        self.y_vel = vel_to_dog_y + y_rot[0]*vel_to_sheeps_x + y_rot[1]*vel_to_sheeps_y

    def is_visible(self):
        # Fist, check if the dog can see the sheep 
        if sqrt((self.x - self.display.sheepdog.x)**2 + (self.y - self.display.sheepdog.y)**2) > self.display.sheepdog.vision:
            self.visible = False
            return
        for sheep in self.display.sheeps:
            if sheep.id != self.id:
                # Check if the sheep is visible by the dog
                if np.array_equal(self.unit(self.x - self.display.sheepdog.x, self.y - self.display.sheepdog.y), self.unit(sheep.x - self.display.sheepdog.x, sheep.y - self.display.sheepdog.y)) and sqrt((self.x - self.display.sheepdog.x)**2 + (self.y - self.display.sheepdog.y)**2) > sqrt((sheep.x - self.display.sheepdog.x)**2 + (sheep.y - self.display.sheepdog.y)**2):
                    self.visible = False
                    return
        self.visible = True

    def change_color(self):
        if self.visible:
            self.canvas.itemconfig(self.id, fill='green')
        else:
            self.canvas.itemconfig(self.id, fill='blue')

    
    def show_velocity(self):
        # Remove the previous velocity vector
        self.canvas.delete(f'velocity{self.id}')
        # Show the velocity vector
        self.canvas.create_line(self.x, self.y, self.x+self.x_vel*100, self.y+self.y_vel*100, fill='purple', tag=f'velocity{self.id}')

    def simulate(self):
        # Compute the new position
        self.velocity()
        self.move(self.sampling*self.x_vel, self.sampling*self.y_vel)

        # Check if the sheep is visible
        self.is_visible()
        self.change_color()
        self.show_velocity()
        self.canvas.after(100, self.simulate)
