import numpy as np
from physics.physical_object import ObstructingCircle
from mocks.mock_colliders import MockCollidingLine, MockCollidingCircle


def test_circle_line_collision():
    circle_center = np.array((4.1, 3.0))
    circle_radius = 0.2
    circle = ObstructingCircle(circle_center, circle_radius)
    line = MockCollidingLine(np.array((4.0, 2.0)), np.array((4.0, 4.0)))
    collision_point = circle.collide(line)['intersection']
    assert (collision_point == [4.0, 3.0]).all()


def test_circle_line_collision_again():
    circle_center = np.array((2.0, 2.0))
    circle_radius = 1.0
    circle = ObstructingCircle(circle_center, circle_radius)
    line = MockCollidingLine(np.array((0.0, 2.0)), np.array((1.5, 2.0)))
    collision_point = circle.collide(line)['intersection']
    assert (collision_point == [1.5, 2.0]).all()


def test_circle_line_collision_again_again():
    circle_center = np.array((2.0, 2.0))
    circle_radius = 1.0
    circle = ObstructingCircle(circle_center, circle_radius)
    line = MockCollidingLine(np.array((4.0, 2.0)), np.array((2.0, 2.0)))
    collision_point = circle.collide(line)['intersection']
    assert (collision_point == [2.0, 2.0]).all()


def test_circle_circle_collision():
    circle_one_center = np.array((4.0, 4.0))
    circle_one_radius = 1
    circle_two_center = np.array((2.5, 4.0))
    circle_two_radius = 1
    colliding_circle = MockCollidingCircle(circle_one_center, circle_one_radius)
    circle = ObstructingCircle(circle_two_center, circle_two_radius)
    collision = circle.collide(colliding_circle)
    assert (collision['intersection'] == [3.5, 4.0]).all()
    assert (collision['avoid'] == [1, 0]).all()