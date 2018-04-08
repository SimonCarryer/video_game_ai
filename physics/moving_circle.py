import numpy as np
from .constants import *
from util.helpers import *
from moving_object import Moving


class MovingCircle(Moving):
    def __init__(self,
                 initial_location, 
                 initial_velocity=[0, 0],
                 radius=7.5):
        Moving.__init__(self,
                        initial_location, 
                        initial_velocity=initial_velocity)
        self.radius = radius
        self.collide_type = 'circle'

    def get_collisions(self, list_of_screen_objects):
        collisions = []
        for screen_object in list_of_screen_objects:
            collision = screen_object.collide(self)
            if collision is not None:
                collisions.append(collision)
        return collisions

    def vector_from_collision(self, collision_point):
        vector = normalise_vector(self.coords - collision_point)
        return vector * self.radius

    def handle_collisions(self, list_of_screen_objects):
        collision_points = [collision['intersection'] for collision in self.get_collisions(list_of_screen_objects)]
        if len(collision_points) > 0:
            closest_collision_point = find_closest_point(self.coords, collision_points)
            collision_adjustment = self.vector_from_collision(closest_collision_point)
            self.coords = closest_collision_point + collision_adjustment

    def move(self, list_of_screen_objects):
        self.recalculate_velocity()
        self.last_coords = self.coords
        self.coords = (self.velocity / 2) + self.coords
        self.handle_collisions(list_of_screen_objects)
        self.coords = (self.velocity / 2) + self.coords
        self.handle_collisions(list_of_screen_objects)

