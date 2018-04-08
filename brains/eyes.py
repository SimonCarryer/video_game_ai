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
        self.look_ahead = 100

    def get_mouse_position(self):
        return np.array(pygame.mouse.get_pos()).astype(float)

    def look_for_collisions(self, coords, vector, list_of_game_objects):
        ahead_end = coords + (vector * self.look_ahead)
        ahead = EyeBeam(coords, ahead_end)
        return ahead.get_closest_collision(list_of_game_objects)



