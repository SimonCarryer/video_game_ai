import numpy as np
from .constants import *
from .helpers import *


class Moving:
    def __init__(self, 
                 initial_location, 
                 initial_velocity=[0, 0]):
        self.coords = np.array([float(i) for i in initial_location])
        self.velocity = np.array([float(i) for i in initial_velocity])
        self.last_coords = self.coords - self.velocity
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

    def move(self):
        self.recalculate_velocity()
        self.last_coords = self.coords
        self.coords = self.velocity + self.coords
