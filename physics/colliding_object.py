from util.helpers import *
import uuid


class Colliding(object):
    def __init__(self, coords):
        self.name = uuid.uuid4().bytes
        self.coords = coords
        self.collide_type = None

    def get_collisions(self, list_of_screen_objects):
        collisions = []
        for screen_object in list_of_screen_objects:
            collision = screen_object.collide(self)
            if collision is not None:
                collisions.append(collision)
        return collisions

    def get_closest_collision(self, list_of_screen_objects):
        collisions = self.get_collisions(list_of_screen_objects)
        if len(collisions) > 0:
            collision_points = [collision['intersection'] for collision in collisions]
            closest_index = find_closest_point_index(self.coords, collision_points)
            return collisions[closest_index]
        else:
            return None
