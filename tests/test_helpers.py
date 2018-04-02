import numpy as np
from util.helpers import *

vertical_line = (np.array((4.0, 2.0)), np.array((4.0, 4.0)))
horizontal_line = (np.array((2.0, 4.0)), np.array((4.0, 4.0)))
diagonal_line = (np.array((2.0, 2.0)), np.array((4.0, 4.0)))


def test_normalise_vector():
    assert (normalise_vector(np.array([10.0, 0.0])) == [1, 0]).all()
    assert (normalise_vector(np.array([0.0, 6.6])) == [0, 1]).all()
    a = normalise_vector(np.array([9.0, 9.0]))
    b = normalise_vector(np.array([3.0, 3.0]))
    assert (a == b).all()


def test_distance_between_points():
    current = np.array([0.0, 0.0])
    desired = np.array([10.0, 0.0])
    assert distance_between_points(current, desired) == 10.0


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


def test_point_inside_circle():
    circle_center = np.array((10.0, 10.0))
    circle_radius = 5.0
    point_to_test = np.array((12.0, 12.0))
    assert point_inside_circle(circle_center, circle_radius, point_to_test)
    point_to_test = np.array((16.0, 12.0))
    assert not point_inside_circle(circle_center, circle_radius, point_to_test)


def test_closest_point_on_line_vertical():
    point_to_test = np.array((3.0, 3.0))
    closest = closest_point_on_line(vertical_line[0], vertical_line[1], point_to_test)
    assert (closest == [4, 3]).all()


def test_closest_point_on_line_horizontal():
    point_to_test = np.array((3.0, 3.0))
    closest = closest_point_on_line(horizontal_line[0], horizontal_line[1], point_to_test)
    assert (closest == [3, 4]).all()


def test_closest_point_on_line_diagonal():
    point_to_test = np.array((4.0, 3.0))
    closest = closest_point_on_line(diagonal_line[0], diagonal_line[1], point_to_test)
    assert (closest == [3.5, 3.5]).all()


def test_closest_point_on_line_bckwards():
    point_to_test = np.array((3.0, 3.0))
    closest = closest_point_on_line(vertical_line[1], vertical_line[0], point_to_test)
    assert (closest == [4, 3]).all()


def test_closest_point_on_line_oustide_segment():
    point_to_test = np.array((3.0, 5.0))
    closest = closest_point_on_line(vertical_line[0], vertical_line[1], point_to_test)
    assert (closest == [4, 5]).all()


def test_check_if_point_is_on_line():
    point_to_test = np.array((4.0, 3.0))
    assert check_if_point_is_on_line_segment(vertical_line[0], vertical_line[1], point_to_test)
    assert not check_if_point_is_on_line_segment(horizontal_line[0], horizontal_line[1], point_to_test)


def test_circle_line_collision():
    circle_center = np.array((4.1, 3.0))
    circle_radius = 0.2
    assert circle_line_collision(vertical_line[0], vertical_line[1], circle_center, circle_radius)
    circle_center = np.array((4.3, 3.0))
    assert not circle_line_collision(vertical_line[0], vertical_line[1], circle_center, circle_radius)
