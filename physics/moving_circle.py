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

    def possible_collisions(self, list_of_screen_objects):
        walls = just_walls(list_of_screen_objects)
        not_walls = [screen_object for screen_object in list_of_screen_objects if screen_object.image['kind'] != 'wall']
        threatening_walls = filter_threatening_walls(self.coords, self.radius, walls)
        return threatening_walls + not_walls

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
        if magnitude_vector(self.velocity) >= self.radius/2:
            self.coords = (self.velocity / 2) + self.coords
            self.handle_collisions(list_of_screen_objects)
            self.coords = (self.velocity / 2) + self.coords
            self.handle_collisions(list_of_screen_objects)
        else:
            self.coords = (self.velocity) + self.coords
            self.handle_collisions(list_of_screen_objects)

