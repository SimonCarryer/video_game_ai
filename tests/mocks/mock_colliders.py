import numpy as np


class MockCollidingLine:
    def __init__(self, start, end):
        self.start = np.array(start)
        self.end = np.array(end)
        self.collide_type = 'line'


class MockCollidingCircle:
    def __init__(self, coords, radius):
        self.coords = np.array(coords)
        self.radius = radius
        self.collide_type = 'circle'
