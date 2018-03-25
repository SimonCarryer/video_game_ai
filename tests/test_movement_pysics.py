import numpy as np
from physics.moving_object import Moving
from physics.constants import *


def test_moving_object_is_initilised_with_float_coordinates():
    obj = Moving([10, 10])
    assert (obj.coords == np.array([10.0, 10.0])).all()
    assert [i.__class__ for i in obj.coords] == [np.float64, np.float64]


def test_moving_object_is_initialised_with_correct_velocity():
    obj = Moving([10, 10], initial_velocity=[2, 2])
    assert (obj.velocity == np.array([2.0, 2.0])).all()


def test_moving_object_initial_previous_coords_are_set():
    obj = Moving([10, 10], initial_velocity=[2, 2])
    correct_coords = obj.coords - obj.velocity
    assert (correct_coords == np.array([8, 8])).all()


def test_apply_friction_reduces_velocity_magnitude_by_20_percent():
    obj = Moving([10, 10])
    reduced_velocity = obj.apply_friction(np.array([10.0, 0.0]))
    assert (reduced_velocity == np.array([8.0, 0.0])).all()
    reduced_velocity = obj.apply_friction(np.array([0.0, 5.0]))
    assert (reduced_velocity == np.array([0.0, 4.0])).all()
    velocity = np.array([5.0, 6.0])
    speed = np.linalg.norm(velocity)
    reduced_velocity = obj.apply_friction(velocity)
    reduced_speed = np.linalg.norm(reduced_velocity)
    assert reduced_speed == (speed * 0.8)


def test_apply_max_speeds_limits_speed_to_10():
    obj = Moving([10, 10])
    velocity = np.array([20.0, 0.0])
    reduced_velocity = obj.apply_max_speed(velocity)
    assert (reduced_velocity == [10.0, 0.0]).all()
    velocity = np.array([10.0, 10.0])
    reduced_velocity = obj.apply_max_speed(velocity)
    assert np.linalg.norm(reduced_velocity) == 10


def test_recalculate_velocity_adds_accelleration():
    obj = Moving([10, 10], initial_velocity=[1, 1])
    obj.accelleration = np.array([1.0, 0.0])
    obj.recalculate_velocity()
    assert (obj.velocity == np.array([1.6, 0.8])).all()
