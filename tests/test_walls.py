import numpy as np
from physics.physical_object import ObstructingLine
from physics.moving_circle import MovingCircle
from mocks.mock_colliders import MockCollidingLine
from util.helpers import *


def test_line_circle_collide_returns_intersection_point():
    circle_center = np.array((4.1, 3.0))
    circle_radius = 0.2
    line = ObstructingLine(np.array((4.0, 2.0)), np.array((4.0, 4.0)))
    circle = MovingCircle(circle_center, radius=circle_radius)
    collision_point = line.collide(circle)['intersection']
    assert (collision_point == [4.0, 3.0]).all()


def test_line_circle_collide_returns_none():
    circle_center = np.array((4.3, 3.0))
    circle_radius = 0.2
    line = ObstructingLine(np.array((4.0, 2.0)), np.array((4.0, 4.0)))
    circle = MovingCircle(circle_center, radius=circle_radius)
    collision_point = line.collide(circle)
    assert collision_point is None


def test_line_collide_returns_intersection_point():
    colliding_line = MockCollidingLine((3.0, 3.0), (5.0, 3.0))
    line = ObstructingLine(np.array((4.0, 2.0)), np.array((4.0, 4.0)))
    collision_point = line.collide(colliding_line)['intersection']
    assert (collision_point == [4.0, 3.0]).all()


def test_line_collide_with_center_returns_avoid_vector():
    colliding_line = MockCollidingLine((3.0, 3.0), (5.0, 3.0))
    line = ObstructingLine(np.array((4.0, 2.0)), np.array((3.0, 4.0)))
    avoid = line.collide(colliding_line)['avoid']
    assert (avoid == [0, 0]).all()


def test_line_collide_returns_avoid_vector():
    colliding_line = MockCollidingLine((3.0, 3.0), (5.0, 3.0))
    line = ObstructingLine(np.array((4.0, 6.0)), np.array((4.0, 2.0)))
    avoid = line.collide(colliding_line)['avoid']
    assert (avoid == [0, -1]).all()


def test_line_collide_returns_none():
    colliding_line = MockCollidingLine((3.0, 5.0), (5.0, 5.0))
    line = ObstructingLine(np.array((4.0, 2.0)), np.array((4.0, 4.0)))
    collision_point = line.collide(colliding_line)
    assert collision_point is None


def test_collision_with_other_object_returns_none():
    line = ObstructingLine(np.array((4.0, 2.0)), np.array((4.0, 4.0)))
    other_line = ObstructingLine(np.array((3.0, 3.0)), np.array((6.0, 3.0)))
    collision_point = line.collide(other_line)
    assert collision_point is None


def test_avoid_vector():
    # vertical line hit at bottom end
    line = ObstructingLine(np.array((4.0, 2.0)), np.array((4.0, 5.0)))
    collision_point = np.array((4.0, 4.0))
    assert (line.avoid_vector(collision_point) == [0, 1]).all()
    # vertical line hit at top end
    line = ObstructingLine(np.array((4.0, 2.0)), np.array((4.0, 5.0)))
    collision_point = np.array((4.0, 2.5))
    assert (line.avoid_vector(collision_point) == [0, -1]).all()
    # horizontal line hit on left side
    line = ObstructingLine(np.array((2.0, 2.0)), np.array((5.0, 2.0)))
    collision_point = np.array((3.0, 2.0))
    assert (line.avoid_vector(collision_point) == [-1, 0]).all()
    # horizontal line hit on right side
    line = ObstructingLine(np.array((2.0, 2.0)), np.array((5.0, 2.0)))
    collision_point = np.array((4.0, 2.0))
    assert (line.avoid_vector(collision_point) == [1, 0]).all()
    # diagonal line hit on top left
    line = ObstructingLine(np.array((2.0, 2.0)), np.array((5.0, 5.0)))
    collision_point = np.array((3.0, 3.0))
    avoid = line.avoid_vector(collision_point)
    correct = normalise_vector(np.array([-1.0, -1.0]))
    assert (avoid == correct).all()
