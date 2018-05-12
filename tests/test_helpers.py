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
    line_start = np.array((1.0, 3.0))
    line_end = np.array((3.0, 3.0))
    intersection = find_intersecting_point(vertical_line[0],
                                           vertical_line[1],
                                           line_start,
                                           line_end)
    assert (intersection == [4.0, 3.0]).all()


def test_intersecting_backwards_lines_returns_intersection_point():
    line_start = np.array((1.0, 3.0))
    line_end = np.array((3.0, 3.0))   
    intersection = find_intersecting_point(vertical_line[1],
                                           vertical_line[0],
                                           line_end,
                                           line_start)
    assert (intersection == [4.0, 3.0]).all()


def test_check_for_line_intersection_finds_true_intesections():
    line_one_start = np.array((2.0, 2.0))
    line_one_end = np.array((2.0, 4.0))
    line_two_start = np.array((1.0, 3.0))
    line_two_end = np.array((3.0, 3.0))
    assert check_for_line_intersection(line_one_start,
                                       line_one_end,
                                       line_two_start,
                                       line_two_end)


def test_lines_just_touching_right():
    line_one_start = np.array((3.0, 1.0))
    line_one_end = np.array((3.0, 3.0))
    line_two_start = np.array((1.0, 2.0))
    line_two_end = np.array((3.0, 2.0))
    assert check_for_line_intersection(line_one_start,
                                       line_one_end,
                                       line_two_start,
                                       line_two_end)


def test_lines_just_touching_left():
    line_one_start = np.array((1.0, 1.0))
    line_one_end = np.array((1.0, 3.0))
    line_two_start = np.array((1.0, 2.0))
    line_two_end = np.array((3.0, 2.0))
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
    collision_point = circle_line_collision(vertical_line[0], vertical_line[1], circle_center, circle_radius)
    assert (collision_point == [4.0, 3.0]).all()
    circle_center = np.array((4.3, 3.0))
    collision_point = circle_line_collision(vertical_line[0], vertical_line[1], circle_center, circle_radius)
    assert collision_point is None


def test_circle_line_collision_with_end_point():
    circle_center = np.array((4.0, 4.1))
    circle_radius = 0.2
    collision_point = circle_line_collision(vertical_line[0], vertical_line[1], circle_center, circle_radius)
    assert (collision_point == [4.0, 4.0]).all()
    circle_center = np.array((4.0, 4.3))
    collision_point = circle_line_collision(vertical_line[0], vertical_line[1], circle_center, circle_radius)
    assert collision_point is None


def test_line_normal_returns_perpendicular_line():
    vertical_line = (np.array((4.0, 2.0)), np.array((4.0, 4.0)))
    normal = line_normal(vertical_line[0], vertical_line[1])
    assert (normal[0] == [(-0.0, 2.0)]).all()
    assert (normal[1] == [(0.0, -2.0)]).all()


def test_random_vector():
    randoms = [random_vector() for _ in range(2000)]
    assert 0.9 <= max([a for a, b in randoms]) <= 1
    assert -1 <= min([a for a, b in randoms]) <= -0.9
    assert 1.4 <= max([a + b for a, b in randoms]) <= 1.42
    assert -1.42 <= min([a + b for a, b in randoms]) <= -1.4


def test_circle_circle_collision():
    circle_one_center = np.array((4.0, 4.0))
    circle_one_radius = 1
    circle_two_center = np.array((2.5, 4.0))
    circle_two_radius = 1
    intersection = circle_circle_collision(circle_one_center,
                                           circle_one_radius,
                                           circle_two_center,
                                           circle_two_radius)
    assert (intersection == [3.5, 4.0]).all()


def test_divide_by_zero():
    zero_array = np.array((0.0, 0.0))
    assert (perpendicular_vector(zero_array) == zero_array).all()
    assert (normalise_vector(zero_array) == zero_array).all()
    assert (dot(zero_array, zero_array, zero_array) == zero_array).all()
    ones_array = np.array((1.0, 1.0))
    twos_array = np.array((2.0, 2.0))
    assert (find_intersecting_point(zero_array, ones_array, ones_array, twos_array) == ones_array).all()
    assert (find_intersecting_point(ones_array, zero_array, zero_array, twos_array) == zero_array).all()
