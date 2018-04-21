import numpy as np
from .constants import *
from util.helpers import *
from moving_object import Moving


class MovingCircle(Moving):
    def __init__(self,
                 initial_location, 
                 initial_velocity=[0, 0],
                 max_accelleration=3,
                 radius=7.5):
        Moving.__init__(self,
                        initial_location,
                        max_accelleration=max_accelleration,
                        initial_velocity=initial_velocity)
        self.radius = radius
        self.collide_type = 'circle'

    def vector_from_collision(self, collision_point):
        vector = normalise_vector(self.coords - collision_point)
        return vector * self.radius

    def handle_collisions(self, list_of_screen_objects):
        closest_collision = self.get_closest_collision(list_of_screen_objects)
        if closest_collision is not None:
            collision_point = closest_collision['intersection']
            collision_adjustment = self.vector_from_collision(collision_point)
            self.coords = collision_point + collision_adjustment

    def move(self, list_of_screen_objects):
        self.recalculate_velocity()
        self.last_coords = self.coords
        self.coords = (self.velocity / 2) + self.coords
        self.handle_collisions(list_of_screen_objects)
        self.coords = (self.velocity / 2) + self.coords
        self.handle_collisions(list_of_screen_objects)

