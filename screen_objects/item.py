from drawing.visible import Visible
from physics.physical_object import ObstructingCircle
from .screen_object import ScreenObject
from util.helpers import distance_between_points
import numpy as np


class Item(ScreenObject):
    def __init__(self, coords, colour):
        super(Item, self).__init__()
        self.radius = 5
        self.image = {'kind': 'item', 'colour': colour}
        self.start_coords = np.array(coords)
        self.sprite = Visible(coords,
                              self.radius,
                              colour=colour)

    def collide(self, colliding_object):
        return None

    def coords(self):
        return self.start_coords

    def update(self, screen, list_of_game_objects):
        self.sprite.draw(self.coords(), screen)
