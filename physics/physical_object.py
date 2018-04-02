import numpy as np
from util.helpers import *


class ObstructingLine:
    def __init__(self, start, end):
        self.start = np.array(start)
        self.end = np.array(end)

    def collide(self, colliding_object):
        if colliding_object.__class__.__name__ == 'MovingCircle':
            return self.collide_with_circle(colliding_object.coords,
                                            colliding_object.radius)
        else:
            return None

    def collide_with_circle(self, circle_coords, circle_radius):
        return circle_line_collision(self.start, 
                                     self.end, 
                                     circle_coords, 
                                     circle_radius)
