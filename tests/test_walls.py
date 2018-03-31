import numpy as np
from physics.physical_object import PhysicalWall


def test_wall_collide_returns_intersection_point():
    line_one_start = np.array((2.0, 2.0))
    line_one_end = np.array((2.0, 4.0))
    line_two_start = np.array((1.0, 3.0))
    line_two_end = np.array((3.0, 3.0))
    wall = PhysicalWall(line_one_start, line_one_end)
    intersection = wall.collide(line_two_start, line_two_end)
    assert (intersection == [2.0, 3.0]).all()


def test_wall_collide_returns_none_when_no_collision():
    line_one_start = np.array((4.0, 4.0))
    line_one_end = np.array((4.0, 8.0))
    line_two_start = np.array((1.0, 3.0))
    line_two_end = np.array((3.0, 3.0))
    wall = PhysicalWall(line_one_start, line_one_end)
    intersection = wall.collide(line_two_start, line_two_end)
    assert intersection is None
