from screen_objects.screen_object import ScreenObject
from drawing.visible import VisibleLine
from physics.physical_object import ObstructingLine
from util.helpers import distance_between_points


class Wall(ScreenObject):
    def __init__(self, start, end):
        super(Wall, self).__init__()
        self.sprite = VisibleLine(start, end)
        self.substance = ObstructingLine(start, end)
        self.start = self.substance.start
        self.end = self.substance.end
        self.length = distance_between_points(self.start, self.end)
        self.image['kind'] = 'wall'

    def update(self, screen, list_of_walls):
        self.sprite.draw(screen)

    def coords(self):
        return self.substance.center

    def collide(self, colliding_object):
        return self.substance.collide(colliding_object)


class Boundary(ScreenObject):
    def __init__(self, start, end):
        super(Boundary, self).__init__()
        self.sprite = VisibleLine(start, end)
        self.substance = ObstructingLine(start, end)
        self.substance.avoid_vector = lambda x: (0, 0)
        self.start = self.substance.start
        self.end = self.substance.end
        self.length = distance_between_points(self.start, self.end)
        self.image['kind'] = 'wall'

    def coords(self):
        return self.substance.center

    def update(self, screen, list_of_walls):
        pass

    def collide(self, colliding_object):
        return self.substance.collide(colliding_object)