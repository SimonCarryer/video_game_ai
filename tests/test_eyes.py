from brains.eyes import Eyes, EyeBeam
from physics.physical_object import ObstructingLine
import numpy as np


def test_eyes_see_collision():
    eyes = Eyes()
    wall = ObstructingLine(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    coords = np.array((1.0, 3.0))
    vector = np.array((1.0, 0.0))
    collision = eyes.look_for_collisions(coords, vector, 0, 'abc', [wall])
    assert (collision['avoid'] == [0, -1]).all()
    assert (collision['intersection'] == [2, 3]).all()