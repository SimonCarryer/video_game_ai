import pygame
import numpy as np
from util.helpers import *
from physics.colliding_object import Colliding


class EyeBeam(Colliding):
    def __init__(self, start, end):
        self.start = np.array(start)
        super(EyeBeam, self).__init__(self.start)
        self.end = np.array(end)
        self.collide_type = 'line'


class Eyes:
    def __init__(self):
        self.look_ahead = 10

    def get_mouse_position(self):
        return np.array(pygame.mouse.get_pos()).astype(float)

    def look_for_collisions(self, coords, vector, radius, list_of_screen_objects):
        for sign in [1.0, 0.0, -1.0]:
            adjustment = normalise_vector(perpendicular_vector(vector)) * (sign * radius)
            adjusted_coords = coords + adjustment
            ahead_end = adjusted_coords + (vector * self.look_ahead)
            ahead = EyeBeam(adjusted_coords, ahead_end)
            collision = ahead.get_closest_collision(list_of_screen_objects)
            if collision is not None:
                return collision
        return None

    def look_at_object(self, coords, screen_object, list_of_screen_objects):
        ray = EyeBeam(coords, screen_object.coords())
        collisions = ray.get_collisions(list_of_screen_objects)
        if len(collisions) == 1:
            return collisions[0]
        else:
            return None

    def visible_objects(self, coords, list_of_screen_objects):
        visibles = []
        for screen_object in list_of_screen_objects:
            eyes_see = self.look_at_object(coords,
                                           screen_object,
                                           list_of_screen_objects)
            if eyes_see is not None:
                visibles.append(eyes_see)
        return visibles

    def look_for_object(self,
                        coords,
                        distance,
                        object_description,
                        list_of_screen_objects):
        matching_objects_in_range = [screen_object for screen_object in \
                            list_of_screen_objects \
                            if distance_between_points(coords, screen_object.coords()) < distance \
                            and object_description.viewitems() <= screen_object.image.viewitems()]
        if len(matching_objects_in_range) > 0:
            closest_index = find_closest_point_index(coords, [screen_object.coords() for screen_object in matching_objects_in_range])
            target_object = matching_objects_in_range[closest_index]
            return self.look_at_object(coords, target_object, list_of_screen_objects)
        return None

        
