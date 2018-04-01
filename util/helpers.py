import numpy as np
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import euclidean_distances


def normalise_vector(vector):
    return normalize(vector.reshape(1, -1))[0]


def magnitude_vector(vector):
    return np.linalg.norm(vector)


def distance_to_target(current, target):
    return np.linalg.norm(target-current)


def perpendicular_segment(line_segment_a) :
    line_segment_b = np.empty_like(line_segment_a)
    line_segment_b[0] = -line_segment_a[1]
    line_segment_b[1] = line_segment_a[0]
    return line_segment_b


def find_intersecting_point(line_a_start,
                            line_a_end,
                            line_b_start,
                            line_b_end):
    da = line_a_end - line_a_start
    db = line_b_end - line_b_start
    dp = line_a_start - line_b_start
    dap = perpendicular_segment(da)
    denom = np.dot(dap, db)
    num = np.dot(dap, dp)
    return (num / denom.astype(float)) * db + line_b_start


def counterclockwise_points(point_a, point_b, point_c):
    a = (point_c[1] - point_a[1]) * (point_b[0] - point_a[0])
    b = (point_b[1] - point_a[1]) * (point_c[0] - point_a[0])
    return a > b


def check_for_line_intersection(line_a_start,
                                line_a_end,
                                line_b_start,
                                line_b_end):
    a = counterclockwise_points(line_a_start, line_b_start, line_b_end)
    b = counterclockwise_points(line_a_end, line_b_start, line_b_end)
    c = counterclockwise_points(line_a_start, line_a_end, line_b_start)
    d = counterclockwise_points(line_a_start, line_a_end, line_b_end)
    return a != b and c != d


def find_closest_point(origin, list_of_points):
    origin = origin.reshape(1, -1)
    closest_index = euclidean_distances(origin, list_of_points).argmin()
    return list_of_points[closest_index]


def check_for_collisions(start, end, list_of_walls):
    collision_points = []
    for wall in list_of_walls:
        collision_point = wall.collide(start, end)
        if collision_point is not None:
            collision_points.append(collision_point)
    return collision_points


def get_closest_collision_point(start, end, list_of_walls):
    collision_points = check_for_collisions(start, end, list_of_walls)
    if collision_points:
        if len(collision_points) > 1:
            closest_collision_point = find_closest_point(start, 
                                                         collision_points)
        else:
            closest_collision_point = collision_points[0]
    else:
        closest_collision_point = None
    return closest_collision_point
