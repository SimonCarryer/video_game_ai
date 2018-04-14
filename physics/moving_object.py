import numpy as np
from .constants import *
from util.helpers import *
from colliding_object import Colliding


class Moving(Colliding):
    def __init__(self, 
                 initial_location, 
                 initial_velocity=[0, 0]):
        self.coords = np.array(initial_location).astype(float)
        super(Moving, self).__init__(self.coords)
        self.velocity = np.array(initial_velocity).astype(float)
        self.last_coords = self.coords - self.velocity
        self.max_accelleration = 3
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

    def move(self, list_of_walls):
        self.recalculate_velocity()
        self.last_coords = self.coords
        self.coords = self.velocity + self.coords  
