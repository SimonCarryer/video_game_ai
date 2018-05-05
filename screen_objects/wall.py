from drawing.visible import VisibleLine
from physics.physical_object import ObstructingLine


class Wall:
    def __init__(self, start, end):
        self.sprite = VisibleLine(start, end)
        self.substance = ObstructingLine(start, end)
        self.start = start
        self.end = end
        self.image = {}

    def update(self, screen, list_of_walls):
        self.sprite.draw(screen)

    def coords(self):
        return self.substance.center

    def collide(self, colliding_object):
        return self.substance.collide(colliding_object)


class Boundary:
    def __init__(self, start, end):
        self.substance = ObstructingLine(start, end)
        self.start = start
        self.end = end
        self.image = {}

    def coords(self):
        return self.substance.center

    def update(self, screen, list_of_walls):
        pass

    def collide(self, colliding_object):
        return self.substance.collide(colliding_object)
