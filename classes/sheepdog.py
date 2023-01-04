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
        """Return True if the point (x2, y2) is on the left side of the line (x1, y1) -> (0, 0)
        
        Parameters
        ----------
        x1, y1 : float
            The coordinates of the first point
        x2, y2 : float
            The coordinates of the second point
            
        Returns
        -------
        bool
            True if the point (x2, y2) is on the left side of the line (x1, y1) -> (0, 0)"""
        unit_1 = self.unit(x1, y1)
        unit_2 = self.unit(x2, y2)
        return self.find_rotation_angle(unit_1, unit_2) > math.pi/2

    def is_right_side(self, x1, y1, x2, y2):
        """Return True if the point (x2, y2) is on the right side of the line (x1, y1) -> (0, 0)

        Parameters
        ----------
        x1, y1 : float
            The coordinates of the first point
        x2, y2 : float
            The coordinates of the second point

        Returns
        -------
        bool
            True if the point (x2, y2) is on the right side of the line (x1, y1) -> (0, 0)"""
        unit_1 = self.unit(x1, y1)
        unit_2 = self.unit(x2, y2)
        return self.find_rotation_angle(unit_1, unit_2) < math.pi/2

    def find_rotation_angle(self, v1, v2):
        """Find the angle between two vectors

        Parameters
        ----------
        v1 : np.array
            The first vector
        v2 : np.array
            The second vector

        Returns
        -------
        float
            The angle between the two vectors in radians, from 0 to 2*pi"""
        v1_unit = v1 / np.linalg.norm(v1)
        v2_unit = v2 / np.linalg.norm(v2)
        
        # Find the angle between the vectors
        dot = np.dot(v1_unit, v2_unit)
        if dot > 1:
            angle = 0
        else :
            angle = math.acos(dot)
        
        # Check the direction of the rotation
        if v1_unit[0]*v2_unit[1] - v1_unit[1]*v2_unit[0] < 0:
            angle *= -1
    
        return angle % 2*math.pi

    def rotate(self, x, y, angle):
        """Rotate a vector (x, y) by an angle

        Parameters
        ----------
        x, y : float
            The coordinates of the vector to rotate
        angle : float
            The angle to rotate the vector by in radians
        
        Returns
        -------
        np.array
            The coordinates of the rotated vector"""
        return np.array([x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle)])

    def find_rightmost_sheep_from_dog(self):
        rightmost_sheep_from_barn = None
        for sheep in self.display.sheeps :
            if rightmost_sheep_from_barn == None:
                rightmost_sheep_from_barn = sheep
            elif self.is_right_side(sheep.x-self.display.barn.x, sheep.y-self.display.barn.y, rightmost_sheep_from_barn.x-self.display.barn.x, rightmost_sheep_from_barn.y-self.display.barn.y):
                rightmost_sheep_from_barn = sheep
        return rightmost_sheep_from_barn

    def find_leftmost_sheep_from_dog(self):
        leftmost_sheep_from_dog = None
        for sheep in self.display.sheeps :
            if leftmost_sheep_from_dog == None:
                leftmost_sheep_from_dog = sheep
            elif self.is_left_side(sheep.x-self.x, sheep.y-self.y, leftmost_sheep_from_dog.x-self.x, leftmost_sheep_from_dog.y-self.y):
                leftmost_sheep_from_dog = sheep
        return leftmost_sheep_from_dog

    def find_rightmost_sheep_from_barn(self):
        rightmost_sheep_from_dog = None
        for sheep in self.display.sheeps :
            if rightmost_sheep_from_dog == None:
                rightmost_sheep_from_dog = sheep
            elif self.is_right_side(sheep.x-self.x, sheep.y-self.y, rightmost_sheep_from_dog.x-self.x, rightmost_sheep_from_dog.y-self.y):
                rightmost_sheep_from_dog = sheep
        return rightmost_sheep_from_dog

    def find_leftmost_sheep_from_barn(self):
        leftmost_sheep_from_barn = None
        for sheep in self.display.sheeps :
            if leftmost_sheep_from_barn == None:
                leftmost_sheep_from_barn = sheep
            elif self.is_left_side(sheep.x-self.display.barn.x, sheep.y-self.display.barn.y, leftmost_sheep_from_barn.x-self.display.barn.x, leftmost_sheep_from_barn.y-self.display.barn.y):
                leftmost_sheep_from_barn = sheep
        return leftmost_sheep_from_barn

    def count_sheeps_in_barn(self):
        sheeps_in_barn = 0
        for sheep in self.display.sheeps:
            if self.display.barn.is_inside(sheep.x, sheep.y):
                sheeps_in_barn += 1
        return sheeps_in_barn

    def find_sheepherd_center(self):
            # Compute sheepherd_center as the sum of the coordinates of all visible sheeps over the number of visible sheeps
            sheepherd_center = np.array([0, 0])
            visible_sheeps = 0
            for sheep in self.display.sheeps :
                if sheep.visible:
                    sheepherd_center += np.array([sheep.x, sheep.y])
                    visible_sheeps += 1
            if visible_sheeps != 0:
                sheepherd_center /= visible_sheeps
            return sheepherd_center

    def velocity(self):
        """Change the velocity of the sheepdog
        """
        sheeps_in_barn = self.count_sheeps_in_barn()
        if sheeps_in_barn != len(self.display.sheeps):
            dir_self_to_barn = self.unit(self.display.barn.x-self.x, self.display.barn.y-self.y)
            # Check if all sheeps are on the left of dir_self_to_barn
            all_sheeps_on_left = True
            all_sheeps_on_right = True
            for sheep in self.display.sheeps:
                dir_self_to_sheep = self.unit(sheep.x-self.x, sheep.y-self.y)
                if self.is_left_side(*dir_self_to_barn, *dir_self_to_sheep):
                    all_sheeps_on_left = False
                if self.is_right_side(*dir_self_to_barn, *dir_self_to_sheep):
                    all_sheeps_on_right = False
                if not all_sheeps_on_left and not all_sheeps_on_right:
                    break

            # Compute "important" sheeps, i.e. leftmost and righmost sheeps from barn and dog
            leftmost_sheep_from_barn = self.find_leftmost_sheep_from_barn()
            rightmost_sheep_from_barn = self.find_rightmost_sheep_from_barn()
            leftmost_sheep_from_dog = self.find_leftmost_sheep_from_dog()
            rightmost_sheep_from_dog = self.find_rightmost_sheep_from_dog()

            sheepherd_center = self.find_sheepherd_center()

            # Compute L_c = <D^(cd), (x,y)-(leftmost_sheep_from_barn.x, leftmost_sheep_from_barn.y)>/||D^(cd)||.||(x,y)-(leftmost_sheep_from_barn.x, leftmost_sheep_from_barn.y)|| with D^(cd) = unit vector from the sheepherd center to the barn
            dir_sheepherd_center_to_barn = self.unit(self.display.barn.x-sheepherd_center[0], self.display.barn.y-sheepherd_center[1])
            dir_sheepherd_center_to_sheepdog = self.x-sheepherd_center[0], self.y-sheepherd_center[1]
            L_c = np.dot(dir_sheepherd_center_to_barn, dir_sheepherd_center_to_sheepdog) / (np.linalg.norm(dir_sheepherd_center_to_barn) * np.linalg.norm(dir_sheepherd_center_to_sheepdog)) % (2*math.pi)

            # Compute R_c = <D^(cd), (x,y)-(rightmost_sheep_from_barn.x, rightmost_sheep_from_barn.y)>/||D^(cd)||.||(x,y)-(rightmost_sheep_from_barn.x, rightmost_sheep_from_barn.y)|| with D^(cd) = unit vector from the sheepherd center to the barn
            dir_sheepherd_center_to_barn = self.unit(self.display.barn.x-sheepherd_center[0], self.display.barn.y-sheepherd_center[1])
            dir_sheepherd_center_to_sheepdog = self.x-sheepherd_center[0], self.y-sheepherd_center[1]
            R_c = np.dot(dir_sheepherd_center_to_barn, dir_sheepherd_center_to_sheepdog) / (np.linalg.norm(dir_sheepherd_center_to_barn) * np.linalg.norm(dir_sheepherd_center_to_sheepdog)) % (2*math.pi)

            print("all_sheeps_on_left: ", all_sheeps_on_left)
            print("all_sheeps_on_right: ", all_sheeps_on_right)
            print("L_c: ", L_c)
            print("R_c: ", R_c)
            if all_sheeps_on_left and L_c > self.angle_threshold:
                print("state left")
                print()
                self.state = 0
                # if the distance between the sheepdog and the rightmost sheep is more than ra...
                if self.distance(rightmost_sheep_from_barn.x, rightmost_sheep_from_barn.y) >= self.radius_threshold:
                    print("distance rightmost sheepdog > ra")
                    self.x_vel, self.y_vel = self.inradius_gain*self.unit(self.x-rightmost_sheep_from_barn.x, self.y-rightmost_sheep_from_barn.y)
                else:
                    print("distance rightmost sheepdog < ra")
                    self.x_vel, self.y_vel = self.outradius_gain*self.rotate(*self.unit(self.display.barn.x-rightmost_sheep_from_barn.x, self.display.barn.y-rightmost_sheep_from_barn.y), self.rot_right)
            elif all_sheeps_on_right and R_c > self.angle_threshold:
                print("state right")
                print()
                self.state = 1
                # if the distance between the sheepdog and the leftmost sheep is more than ra...
                if self.distance(leftmost_sheep_from_barn.x, leftmost_sheep_from_barn.y) >= self.radius_threshold:
                    self.x_vel, self.y_vel = self.inradius_gain*self.unit(self.x-leftmost_sheep_from_barn.x, self.y-leftmost_sheep_from_barn.y)
                else:
                    self.x_vel, self.y_vel = self.outradius_gain*self.rotate(*self.unit(self.display.barn.x-leftmost_sheep_from_barn.x, self.display.barn.y-leftmost_sheep_from_barn.y), -self.rot_left)
            elif self.state == 1:
                if self.distance(leftmost_sheep_from_barn.x, leftmost_sheep_from_barn.y) >= self.radius_threshold:
                    self.x_vel, self.y_vel = self.inradius_gain*self.unit(self.x-leftmost_sheep_from_barn.x, self.y-leftmost_sheep_from_barn.y)
                else:
                    self.x_vel, self.y_vel = self.outradius_gain*self.rotate(*self.unit(self.display.barn.x-leftmost_sheep_from_barn.x, self.display.barn.y-leftmost_sheep_from_barn.y), -self.rot_left)
            else:
                if self.distance(rightmost_sheep_from_barn.x, rightmost_sheep_from_barn.y) >= self.radius_threshold:
                    self.x_vel, self.y_vel = self.inradius_gain*self.unit(self.x-rightmost_sheep_from_barn.x, self.y-rightmost_sheep_from_barn.y)
                else:
                    self.x_vel, self.y_vel = self.outradius_gain*self.rotate(*self.unit(self.display.barn.x-rightmost_sheep_from_barn.x, self.display.barn.y-rightmost_sheep_from_barn.y), self.rot_right)
        else :
            self.x_vel, self.y_vel = 0, 0

    def show_velocity(self):
        # Remove the previous velocity vector
        self.canvas.delete(f'velocity{self.id}')
        # Show the velocity vector
        self.canvas.create_line(self.x, self.y, self.x+self.x_vel, self.y+self.y_vel, fill='purple', tag=f'velocity{self.id}')

    def simulate(self):
        self.velocity()
        self.move(self.sampling*self.x_vel, self.sampling*self.y_vel)
        self.show_velocity()
        self.canvas.after(25, self.simulate)