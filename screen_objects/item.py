from drawing.visible import Visible
from physics.physical_object import ObstructingCircle
from .screen_object import ScreenObject
from util.helpers import distance_between_points
import numpy as np


class Item(ScreenObject):
    def __init__(self, coords, colour):
        super(Item, self).__init__()
        self.image = {'kind': 'item', 'colour': colour}
        self.start_coords = np.array(coords)
        self.sprite = Visible(coords,
                              5,
                              colour=colour)

    def collide(self, colliding_object):
        return None

    def coords(self):
        return self.start_coords

    def get_picked_up(self, list_of_game_objects):
        boys = [obj for obj in list_of_game_objects if obj.image.get('kind') == 'boy']
        for boy in boys:
            if distance_between_points(self.start_coords, boy.coords()) <= boy.image.get('radius'):
                self.delete = True

    def update(self, screen, list_of_game_objects):
        self.get_picked_up(list_of_game_objects)
        self.sprite.draw(self.coords(), screen)
