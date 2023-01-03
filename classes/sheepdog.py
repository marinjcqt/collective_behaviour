from entity import Entity
import math
import numpy as np
from enum import Enum
class Sheepdog(Entity):

    
    def __init__(self, canvas, x, y, vision, angle_threshold, radius_threshold, rot_left, rot_right, inradius_gain, outradius_gain, sampling, r=5, color='red'):
        super().__init__(canvas, x, y, r, color)
        self.vision = vision
        self.angle_threshold = angle_threshold
        self.state = 1
        self.rot_left = rot_left
        self.rot_right = rot_right
        self.radius_threshold = radius_threshold
        self.inradius_gain = inradius_gain
        self.outradius_gain = outradius_gain
        self.sampling = sampling

    def is_left_side(self, x1, y1, x2, y2):
        unit_1 = self.unit(x1, y1)
        unit_2 = self.unit(x2, y2)

    def find_rotation_angle(v1, v2):
        # Normalize the vectors
        v1_unit = v1 / np.linalg.norm(v1)
        v2_unit = v2 / np.linalg.norm(v2)
        
        # Find the angle between the vectors
        angle = math.acos(np.dot(v1_unit, v2_unit))
        
        # Check the direction of the rotation
        if v1_unit[0]*v2_unit[1] - v1_unit[1]*v2_unit[0] < 0:
            angle *= -1
    
        return angle

    def rotate(self, x, y, angle):
        """Rotate a point counterclockwise by a given angle around a given origin. return a np.array"""
        return np.array([x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle)])

    def velocity(self):
        sheeps_in_barn = 0
        for sheep in self.display.sheeps:
            if self.display.barn.is_inside(sheep.x, sheep.y):
                sheeps_in_barn += 1
        if sheeps_in_barn != len(self.display.sheeps):
            print("Sheeps in barn: ", sheeps_in_barn)
            dir_self_to_barn = self.unit(self.display.barn.x-self.x, self.display.barn.y-self.y)
            # Check if all sheeps are on the left of dir_self_to_barn
            all_sheeps_on_left = True
            all_sheeps_on_right = True
            for sheep in self.display.sheeps:
                dir_self_to_sheep = self.unit(sheep.x-self.x, sheep.y-self.y)
                if dir_self_to_sheep[0]*dir_self_to_barn[1] - dir_self_to_sheep[1]*dir_self_to_barn[0] > 0:
                    all_sheeps_on_left = False
                if dir_self_to_sheep[0]*dir_self_to_barn[1] - dir_self_to_sheep[1]*dir_self_to_barn[0] < 0:
                    all_sheeps_on_right = False
                if not all_sheeps_on_left and not all_sheeps_on_right:
                    break

            leftmost_sheep = None
            for sheep in self.display.sheeps :
                print(sheep.id, "...")
                if sheep.visible:
                    print("Sheep is visible")
                    if leftmost_sheep == None:
                        leftmost_sheep = sheep
                    elif sheep.x < leftmost_sheep.x:
                        leftmost_sheep = sheep

            rightmost_sheep = None
            for sheep in self.display.sheeps :
                if sheep.visible:
                    if rightmost_sheep == None:
                        rightmost_sheep = sheep
                    elif sheep.x > rightmost_sheep.x:
                        rightmost_sheep = sheep

            # Compute sheepherd_center as the sum of the coordinates of all visible sheeps over the number of visible sheeps
            sheepherd_center = [0, 0]
            visible_sheeps = 0
            for sheep in self.display.sheeps :
                if sheep.visible:
                    sheepherd_center[0] += sheep.x
                    sheepherd_center[1] += sheep.y
                    visible_sheeps += 1
            if visible_sheeps != 0:
                sheepherd_center[0] /= visible_sheeps
                sheepherd_center[1] /= visible_sheeps

            # Compute L_c = <D^(cd), (x,y)-(leftmost_sheep.x, leftmost_sheep.y)>/||D^(cd)||.||(x,y)-(leftmost_sheep.x, leftmost_sheep.y)|| with D^(cd) = unit vector from the sheepherd center to the barn
            dir_sheepherd_center_to_barn = self.unit(self.display.barn.x-sheepherd_center[0], self.display.barn.y-sheepherd_center[1])
            dir_sheepherd_center_to_sheepdog = self.unit(self.x-sheepherd_center[0], self.y-sheepherd_center[1])
            L_c = np.dot(dir_sheepherd_center_to_barn, dir_sheepherd_center_to_sheepdog) / (np.linalg.norm(dir_sheepherd_center_to_barn) * np.linalg.norm(dir_sheepherd_center_to_sheepdog))

            # Compute R_c = <D^(cd), (x,y)-(rightmost_sheep.x, rightmost_sheep.y)>/||D^(cd)||.||(x,y)-(rightmost_sheep.x, rightmost_sheep.y)|| with D^(cd) = unit vector from the sheepherd center to the barn
            dir_sheepherd_center_to_barn = self.unit(self.display.barn.x-sheepherd_center[0], self.display.barn.y-sheepherd_center[1])
            dir_sheepherd_center_to_sheepdog = self.unit(self.x-sheepherd_center[0], self.y-sheepherd_center[1])
            R_c = np.dot(dir_sheepherd_center_to_barn, dir_sheepherd_center_to_sheepdog) / (np.linalg.norm(dir_sheepherd_center_to_barn) * np.linalg.norm(dir_sheepherd_center_to_sheepdog))


            if all_sheeps_on_left and L_c > self.angle_threshold:
                print("All sheeps on left")
                self.state = 0
                # if the distance between the sheepdog and the rightmost sheep is more than ra...
                if self.distance(rightmost_sheep.x, rightmost_sheep.y) >= self.radius_threshold:
                    self.x_vel, self.y_vel = self.inradius_gain*self.unit(self.x-rightmost_sheep.x, self.y-rightmost_sheep.y)
                else:
                    self.x_vel, self.y_vel = self.outradius_gain*self.rotate(*self.unit(self.display.barn.x-rightmost_sheep.x, self.display.barn.y-rightmost_sheep.y), self.rot_right)
            elif all_sheeps_on_right and R_c > self.angle_threshold:
                print("All sheeps on right")
                self.state = 1
                # if the distance between the sheepdog and the leftmost sheep is more than ra...
                if self.distance(leftmost_sheep.x, leftmost_sheep.y) >= self.radius_threshold:
                    self.x_vel, self.y_vel = self.inradius_gain*self.unit(self.x-leftmost_sheep.x, self.y-leftmost_sheep.y)
                else:
                    self.x_vel, self.y_vel = self.outradius_gain*self.rotate(*self.unit(self.display.barn.x-leftmost_sheep.x, self.display.barn.y-leftmost_sheep.y), -self.rot_left)
            elif self.state == 1:
                print("State 1")
                if self.distance(leftmost_sheep.x, leftmost_sheep.y) >= self.radius_threshold:
                    self.x_vel, self.y_vel = self.inradius_gain*self.unit(self.x-leftmost_sheep.x, self.y-leftmost_sheep.y)
                else:
                    self.x_vel, self.y_vel = self.outradius_gain*self.rotate(*self.unit(self.display.barn.x-leftmost_sheep.x, self.display.barn.y-leftmost_sheep.y), -self.rot_left)
            else:
                print("State 0")
                if self.distance(rightmost_sheep.x, rightmost_sheep.y) >= self.radius_threshold:
                    self.x_vel, self.y_vel = self.inradius_gain*self.unit(self.x-rightmost_sheep.x, self.y-rightmost_sheep.y)
                else:
                    self.x_vel, self.y_vel = self.outradius_gain*self.rotate(*self.unit(self.display.barn.x-rightmost_sheep.x, self.display.barn.y-rightmost_sheep.y), self.rot_right)
        else :
            print("All sheeps are in the barn !")
            self.x_vel, self.y_vel = 0, 0

    def show_velocity(self):
        # Remove the previous velocity vector
        self.canvas.delete(f'velocity{self.id}')
        # Show the velocity vector
        self.canvas.create_line(self.x, self.y, self.x+self.x_vel*100, self.y+self.y_vel*100, fill='purple', tag=f'velocity{self.id}')

    def simulate(self):
        print("Simulate")
        self.velocity()
        self.move(self.sampling*self.x_vel, self.sampling*self.y_vel)
        print("x_vel = ", self.x_vel, "y_vel = ", self.y_vel)
        self.show_velocity()
        self.canvas.after(100, self.simulate)