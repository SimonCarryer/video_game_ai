import numpy as np


class MockCollidingLine:
    def __init__(self, start, end):
        self.start = np.array(start)
        self.end = np.array(end)
        self.collide_type = 'line'
