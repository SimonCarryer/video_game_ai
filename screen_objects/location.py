from .screen_object import ScreenObject
from drawing.visible import VisibleRect
import numpy as np


class Location(ScreenObject):
    def __init__(self, rect, colour=(50, 10, 10), display_name=None):
        super(Location, self).__init__()
        self.display_name = display_name
        self.rect = np.array(rect)
        self.sprite = VisibleRect(rect, colour=colour)
        self.image = {'kind': 'location', 'rect': rect, 'colour': colour}

    def collide(self, colliding_object):
        return None

    def coords(self):
        return self.rect.mean(axis=1)

    def update(self, screen, list_of_game_objects):
        self.sprite.draw(screen)