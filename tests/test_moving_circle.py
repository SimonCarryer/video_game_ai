from physics.moving_circle import MovingCircle
from physics.physical_object import ObstructingLine
from screen_objects.wall import Wall


def test_circle_moves_when_not_colliding():
    circle = MovingCircle([10, 10], initial_velocity=[10, 0], radius=7.5)
    assert (circle.coords == [10, 10]).all()
    circle.move([])
    assert (circle.coords == [18, 10]).all()
    circle.move([])
    assert (circle.coords == [24.4, 10]).all()


def test_circle_stops_when_moving_slowly_into_line():
    circle = MovingCircle([10, 10], initial_velocity=[10, 0], radius=7.5)
    wall = Wall((20.0, 0.0), (20.0, 30.0))
    circle.move([wall])
    assert (circle.coords == [12.5, 10]).all()


def test_circle_stops_when_moving_quickly_into_line():
    circle = MovingCircle([10, 10], initial_velocity=[20, 0], radius=7.5)
    wall = Wall((20.0, 0.0), (20.0, 30.0))
    circle.move([wall])
    assert (circle.coords == [12.5, 10]).all()
