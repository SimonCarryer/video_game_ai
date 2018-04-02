from physics.moving_circle import MovingCircle
from physics.physical_object import ObstructingLine


def test_circle_moves_when_not_colliding():
    circle = MovingCircle([10, 10], initial_velocity=[10, 0], radius=7.5)
    assert (circle.coords == [10, 10]).all()
    circle.move([])
    assert (circle.coords == [18, 10]).all()
    circle.move([])
    assert (circle.coords == [24.4, 10]).all()


def test_circle_stops_when_moving_slowly_into_line():
    circle = MovingCircle([10, 10], initial_velocity=[10, 0], radius=7.5)
    line = ObstructingLine((20.0, 0.0), (20.0, 30.0))
    circle.move([line])
    assert (circle.coords == [12.5, 10]).all()
