import numpy as np
from util.helpers import *


def test_normalise_vector():
    assert (normalise_vector(np.array([10.0, 0.0])) == [1, 0]).all()
    assert (normalise_vector(np.array([0.0, 6.6])) == [0, 1]).all()
    a = normalise_vector(np.array([9.0, 9.0]))
    b = normalise_vector(np.array([3.0, 3.0]))
    assert (a == b).all()


def test_distance_to_target():
    current = np.array([0.0, 0.0])
    desired = np.array([10.0, 0.0])
    assert distance_to_target(current, desired) == 10.0


def test_intersecting_lines_returns_intersection_point():
    line_one_start = np.array((2.0, 2.0))
    line_one_end = np.array((2.0, 4.0))
    line_two_start = np.array((1.0, 3.0))
    line_two_end = np.array((3.0, 3.0))
    intersection = find_intersecting_point(line_one_start,
                                           line_one_end,
                                           line_two_start,
                                           line_two_end)
    assert (intersection == [2.0, 3.0]).all()


def test_check_for_line_intersection_finds_true_intesections():
    line_one_start = np.array((2.0, 2.0))
    line_one_end = np.array((2.0, 4.0))
    line_two_start = np.array((1.0, 3.0))
    line_two_end = np.array((3.0, 3.0))
    assert check_for_line_intersection(line_one_start,
                                       line_one_end,
                                       line_two_start,
                                       line_two_end)


def test_check_for_line_intersection_finds_no_intesections():
    line_one_start = np.array((4.0, 2.0))
    line_one_end = np.array((4.0, 4.0))
    line_two_start = np.array((1.0, 3.0))
    line_two_end = np.array((3.0, 3.0))
    assert not check_for_line_intersection(line_one_start,
                                           line_one_end,
                                           line_two_start,
                                           line_two_end)


def test_find_closest_point():
    origin = np.array((4.0, 2.0))
    point_one = np.array((4.0, 4.0))
    point_two = np.array((1.0, 3.0))
    point_three = np.array((3.0, 3.0))
    closest_point = find_closest_point(origin, 
                                       [point_one, point_two, point_three])
    assert (closest_point == point_three).all()