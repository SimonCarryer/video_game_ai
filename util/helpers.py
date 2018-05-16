import numpy as np
import random
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import euclidean_distances


def normalise_vector(vector):
    if np.isnan(vector).any():
        return np.array((0, 0))
    else:
        return normalize(vector.reshape(1, -1))[0]


def magnitude_vector(vector):
    return np.linalg.norm(vector)


def distance_between_points(current, target):
    return np.linalg.norm(target-current)


def perpendicular_vector(vector_a):
    vector_b = np.empty_like(vector_a).astype(float)
    vector_b[0] = -vector_a[1]
    vector_b[1] = vector_a[0]
    return vector_b


def find_intersecting_point(line_a_start,
                            line_a_end,
                            line_b_start,
                            line_b_end):
    da = line_a_end - line_a_start
    db = line_b_end - line_b_start
    dp = line_a_start - line_b_start
    dap = perpendicular_vector(da)
    denom = np.dot(dap, db)
    num = np.dot(dap, dp)
    if (np.array((denom, num)) == np.array((0, 0))).any():
        if (line_a_start == line_b_start).all():
            return line_a_start
        else:
            return line_a_end
    return (num / denom.astype(float)) * db + line_b_start


def counterclockwise_points(point_a, point_b, point_c):
    a = (point_c[1] - point_a[1]) * (point_b[0] - point_a[0])
    b = (point_b[1] - point_a[1]) * (point_c[0] - point_a[0])
    return a > b


def points_on_line(line_a_start,
                   line_a_end,
                   line_b_start,
                   line_b_end):
    a = check_if_point_is_on_line_segment(line_a_start, line_a_end, line_b_start)
    b = check_if_point_is_on_line_segment(line_a_start, line_a_end, line_b_end)
    c = check_if_point_is_on_line_segment(line_b_start, line_b_start, line_a_start)
    d = check_if_point_is_on_line_segment(line_b_start, line_b_start, line_a_end)
    return a or b or c or d


def check_for_line_intersection(line_a_start,
                                line_a_end,
                                line_b_start,
                                line_b_end):
    a = counterclockwise_points(line_a_start, line_b_start, line_b_end)
    b = counterclockwise_points(line_a_end, line_b_start, line_b_end)
    c = counterclockwise_points(line_a_start, line_a_end, line_b_start)
    d = counterclockwise_points(line_a_start, line_a_end, line_b_end)
    return (a != b and c != d) or points_on_line(line_a_start,
                                                 line_a_end,
                                                 line_b_start,
                                                 line_b_end)


def find_closest_point(origin, list_of_points):
    if len(list_of_points) == 1:
        closest_index = 0
    else:
        origin = origin.reshape(1, -1)
        closest_index = euclidean_distances(origin, list_of_points).argmin()
    return list_of_points[closest_index]


def find_closest_point_index(origin, list_of_points):
    if len(list_of_points) == 1:
        closest_index = 0
    else:
        origin = origin.reshape(1, -1)
        closest_index = euclidean_distances(origin, list_of_points).argmin()
    return closest_index


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


def point_inside_circle(circle_center, circle_radius, point):
    distance = distance_between_points(circle_center, point)
    return distance < circle_radius


def closest_point_on_line(line_start, line_end, point):
    dot_prod = dot(line_start, line_end, point)
    closest_X = line_start[0] + (dot_prod * (line_end[0]-line_start[0]))
    closest_Y = line_start[1] + (dot_prod * (line_end[1]-line_start[1]))
    return np.array((closest_X, closest_Y))


def dot(line_start, line_end, point):
    line_length = distance_between_points(line_start, line_end)
    a = ((point[0]-line_start[0])*(line_end[0]-line_start[0]))
    b = ((point[1]-line_start[1])*(line_end[1]-line_start[1]))
    squared_length = pow(line_length, 2)
    if squared_length > 0:
        return (a + b) / squared_length
    else:
        return np.array((0.0, 0.0))


def check_if_point_is_on_line_segment(line_start, line_end, point):
    buffer = 0.05
    distance_to_start = distance_between_points(point, line_start)
    distance_to_end = distance_between_points(point, line_end)
    line_length = distance_between_points(line_start, line_end)
    total_distance = distance_to_start + distance_to_end
    return (total_distance - buffer) <= line_length <= (total_distance + buffer)


def circle_line_collision(line_start, line_end, circle_center, circle_radius):
    # all this thanks to http://www.jeffreythompson.org/collision-detection/
    closest_point = closest_point_on_line(line_start, line_end, circle_center)
    if distance_between_points(circle_center, closest_point) < circle_radius:
        if check_if_point_is_on_line_segment(line_start, line_end, closest_point):
            return closest_point
    if point_inside_circle(circle_center, circle_radius, line_start):
        return line_start
    if point_inside_circle(circle_center, circle_radius, line_end):
        return line_end
    return None


def line_normal(line_start, line_end):
    dx = line_end[0] - line_start[1]
    dy = line_end[1] - line_start[0]
    normal_start = np.array((-dy, dx))
    normal_end = np.array((dy, -dx))
    return normal_start, normal_end


def center_of_line(line_start, line_end):
    return (line_start + line_end) / 2


def random_vector():
    vector = np.empty(2)
    vector[0] = random.uniform(-1, 1)
    vector[1] = random.uniform(-1, 1)
    return normalise_vector(vector)


def circle_circle_collision(colliding_circle_coords, 
                            colliding_circle_radius,
                            collided_circle_coords,
                            collided_circle_radius):
    distance = distance_between_points(colliding_circle_coords, collided_circle_coords)
    if distance < colliding_circle_radius + collided_circle_radius:
        vector_between_circles = normalise_vector(colliding_circle_coords - collided_circle_coords)
        return collided_circle_coords + vector_between_circles * collided_circle_radius
    else:
        return None


def unobstructed_edges(edges_vector, wall_vector):
    walls_product = np.tile(np.transpose(wall_vector), len(edges_vector))
    edges_product = np.transpose(np.repeat(edges_vector, len(wall_vector), axis=0))
    a = (edges_product[3] - walls_product[1]) * (edges_product[0] - walls_product[0])\
        > (edges_product[1] - walls_product[1]) * (edges_product[2] - walls_product[0])

    b = (edges_product[3] - walls_product[3]) * (edges_product[0] - walls_product[2])\
        > (edges_product[1] - walls_product[3]) * (edges_product[2] - walls_product[2])

    c = (edges_product[1] - walls_product[1]) * (walls_product[2] - walls_product[0])\
        > (walls_product[3] - walls_product[1]) * (edges_product[0] - walls_product[0])

    d = (edges_product[3] - walls_product[1]) * (walls_product[2] - walls_product[0])\
        > (walls_product[3] - walls_product[1]) * (edges_product[2] - walls_product[0])
    intersections = ~((a != b) & (c != d))
    return np.array([i.all() for i in np.split(intersections, len(edges_vector))])
