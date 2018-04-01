import numpy as np
from util.helpers import *


class PhysicalWall:
    def __init__(self, start, end):
        self.start = np.array(start)
        self.end = np.array(end)

    def collide(self, movement_start, movement_end):
        if check_for_line_intersection(self.start,
                                       self.end,
                                       movement_start,
                                       movement_end):
            return find_intersecting_point(self.start,
                                           self.end,
                                           movement_start,
                                           movement_end)
        else:
            return None
