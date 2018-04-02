import numpy as np
from physics.physical_object import ObstructingLine
from physics.moving_circle import MovingCircle


def test_line_circle_collide_returns_intersection_point():
    circle_center = np.array((4.1, 3.0))
    circle_radius = 0.2
    line = ObstructingLine(np.array((4.0, 2.0)), np.array((4.0, 4.0)))
    circle = MovingCircle(circle_center, radius=circle_radius)
    collision_point = line.collide(circle)
    assert (collision_point == [4.0, 3.0]).all()


def test_line_circle_collide_returns_none():
    circle_center = np.array((4.3, 3.0))
    circle_radius = 0.2
    line = ObstructingLine(np.array((4.0, 2.0)), np.array((4.0, 4.0)))
    circle = MovingCircle(circle_center, radius=circle_radius)
    collision_point = line.collide(circle)
    assert collision_point is None


def test_collision_with_other_object_returns_none():
    line = ObstructingLine(np.array((4.0, 2.0)), np.array((4.0, 4.0)))
    other_line = ObstructingLine(np.array((3.0, 3.0)), np.array((6.0, 3.0)))
    collision_point = line.collide(other_line)
    assert collision_point is None