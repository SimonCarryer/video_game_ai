import numpy as np
from .constants import *
from util.helpers import *


class Moving:
    def __init__(self, 
                 initial_location, 
                 initial_velocity=[0, 0]):
        self.coords = np.array([float(i) for i in initial_location])
        self.velocity = np.array([float(i) for i in initial_velocity])
        self.last_coords = self.coords - self.velocity
        self.max_accelleration = 3
        self.buffer = 10
        self.accelleration = np.array([0.0, 0.0])

    def apply_friction(self, velocity):
        opposite_vector = -normalise_vector(velocity)
        magnitude = magnitude_vector(velocity)
        friction_force = magnitude * FRICTION
        friction = opposite_vector * friction_force
        return velocity + friction

    def apply_max_speed(self, velocity):
        speed = magnitude_vector(velocity)
        if speed > MAX_SPEED:
            vector = normalise_vector(velocity)
            velocity = vector * MAX_SPEED
        return velocity

    def apply_min_speed(self, velocity):
        speed = magnitude_vector(velocity)
        if speed < MIN_SPEED:
            velocity = np.array((0, 0))
        return velocity

    def recalculate_velocity(self):
        velocity = self.coords - self.last_coords
        velocity += self.accelleration
        velocity = self.apply_friction(velocity)
        velocity = self.apply_max_speed(velocity)
        velocity = self.apply_min_speed(velocity)
        self.velocity = velocity

    def set_accelleration(self, goal_vector):
        self.accelleration = goal_vector * self.max_accelleration

    def move_up_to_collision_point(self, collision_point):
        self.last_coords = self.coords
        for axis in (0, 1):
            if self.velocity[axis] > 0:
                buffer = -1
            else:
                buffer = 1
            self.coords[axis] = collision_point[axis] + buffer

    def move_without_collision_point(self):
        self.last_coords = self.coords
        self.coords = self.velocity + self.coords

    def collide(self, list_of_walls):
        anticipated_position = self.coords + self.velocity
        collision_point = get_closest_collision_point(self.coords,
                                                      anticipated_position,
                                                      list_of_walls)
        return collision_point

    def move(self, list_of_walls):
        self.recalculate_velocity()
        collision_point = self.collide(list_of_walls)
        if collision_point is not None:
            self.move_up_to_collision_point(collision_point)
        else:
            self.move_without_collision_point()  
