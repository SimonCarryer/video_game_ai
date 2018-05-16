from brains.frontal_lobe import FrontalLobe
from screen_objects.wall import Wall
import numpy as np


def test_populate_grid():
    lobe = FrontalLobe(100, 100, 20)
    lobe.populate_grid([])


def test_closest_node():
    lobe = FrontalLobe(100, 100, 20)
    lobe.populate_grid([])
    position = np.array((0, 21))
    assert lobe.closest_node(position) == (10, 30)


def test_pathfind_goal():
    lobe = FrontalLobe(100, 100, 20)
    lobe.populate_grid([])
    position = np.array((0, 21))
    goal = np.array((81, 71))
    assert (lobe.pathfind_goal(position, goal) == (30, 30)).all()

