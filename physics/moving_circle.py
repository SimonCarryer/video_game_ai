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

    def move(self, list_of_walls):
        self.recalculate_velocity()
        self.last_coords = self.coords
        self.coords = self.velocity + self.coords  