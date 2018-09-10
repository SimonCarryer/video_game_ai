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

    def unobstructed(self, list_of_game_objects):
        walls_vector = walls_vector_from_game_objects(list_of_game_objects)
        edge_vector = np.array((self.start, self.end))
        return unobstructed_edges(edge_vector, walls_vector)[0]


class Eyes:
    def __init__(self):
        self.look_ahead = 10
        self.list_of_game_objects = []

    def update(self, list_of_game_objects):
        self.list_of_game_objects = list_of_game_objects

    def direct_path_to_goal(self, current_position, goal, exclude=[]):
        obstructions = [i for i in self.list_of_game_objects if i not in exclude]
        walls_vector = walls_vector_from_game_objects(obstructions)
        if len(walls_vector) == 0:
            return True
        goal_edge = np.array([[current_position[0], current_position[1], goal[0], goal[1]]])
        return unobstructed_edges(goal_edge, walls_vector)

    def get_mouse_position(self):
        return np.array(pygame.mouse.get_pos()).astype(float)

    def look_for_collisions(self, coords, vector, radius):
        for sign in [1.0, 0.0, -1.0]:
            adjustment = normalise_vector(perpendicular_vector(vector)) * (sign * radius)
            adjusted_coords = coords + adjustment
            ahead_end = adjusted_coords + (vector * self.look_ahead)
            ahead = EyeBeam(adjusted_coords, ahead_end)
            collision = ahead.get_closest_collision(self.list_of_game_objects)
            if collision is not None:
                return collision
        return None

    def look_at_object(self, coords, screen_object):
        if self.direct_path_to_goal(coords, screen_object.coords(), exclude=[screen_object]):
            return screen_object
        else:
            return None

    def visible_objects(self, coords):
        visibles = []
        for screen_object in self.list_of_game_objects:
            eyes_see = self.look_at_object(coords,
                                           screen_object)
            if eyes_see is not None:
                visibles.append(eyes_see)
        return visibles

    def look_for_object(self,
                        coords,
                        distance,
                        object_description):
        matching_objects_in_range = [screen_object for screen_object in \
                            self.list_of_game_objects \
                            if screen_object.image['kind'] != 'wall'
                            and distance_between_points(coords, screen_object.coords()) < distance \
                            and object_description.viewitems() <= screen_object.image.viewitems()]
        if len(matching_objects_in_range) > 0:
            closest_index = find_closest_point_index(coords, [screen_object.coords() for screen_object in matching_objects_in_range])
            target_object = matching_objects_in_range[closest_index]
            return self.look_at_object(coords, target_object)
        return None

        
