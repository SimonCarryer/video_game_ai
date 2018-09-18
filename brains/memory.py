from util.helpers import just_walls
from collections import defaultdict


class DumbMemory:
    def __init__(self, body, eyes):
        self.boy = body
        self.eyes = eyes

    def update(self):
        pass


class Memory:
    def __init__(self, body, eyes):
        self.body = body
        self.eyes = eyes
        self.known_walls = []

    def update(self):
        visible = self.eyes.visible_objects(self.body.coords)
        self.remember_walls(visible)

    def remember_walls(self, list_of_visible_objects):
        walls = just_walls(list_of_visible_objects)
        for wall in walls:
            if wall not in self.known_walls:
                wall.sprite.colour = (0, 0, 220)
                self.known_walls.append(wall)