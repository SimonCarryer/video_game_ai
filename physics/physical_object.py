import numpy as np
from util.helpers import *


class Obstructing(object):
        def collide(self, colliding_object):
            if colliding_object.collide_type == 'circle':
                return self.collide_with_circle(colliding_object.coords,
                                                colliding_object.radius)
            elif colliding_object.collide_type == 'line':
                return self.collide_with_line(colliding_object.start,
                                              colliding_object.end)
            else:
                return None

        def avoid_vector(self, collision_point):
            return normalise_vector(collision_point - self.center)

        def collision(self, intersection, avoid):
            return {'intersection': intersection,
                    'avoid': avoid,
                    'name': 'abc'
                    }


class ObstructingLine(Obstructing):
    def __init__(self, start, end):
        self.start = np.array(start).astype(float)
        self.end = np.array(end).astype(float)
        self.normal_start, self.normal_end = line_normal(self.start, self.end)
        self.center = center_of_line(self.start, self.end)
        self.collide_type = None

    def collide_with_circle(self, circle_coords, circle_radius):
        intersection = circle_line_collision(self.start, 
                                             self.end, 
                                             circle_coords,
                                             circle_radius)
        if intersection is not None:
            avoid = self.avoid_vector(intersection)
            return self.collision(intersection, avoid)
        else:
            return None

    def collide_with_line(self, line_start, line_end):
        if check_for_line_intersection(self.start, self.end, line_start, line_end):
            intersection = find_intersecting_point(self.start, self.end, line_start, line_end)
            avoid = self.avoid_vector(intersection)
            return self.collision(intersection, avoid)
        else:
            return None


class ObstructingCircle(Obstructing):
    def __init__(self, coords, radius):
        self.radius = radius
        self.center = coords

    def collide_with_line(self, line_start, line_end):
        intersection = circle_line_collision(line_start, 
                                             line_end, 
                                             self.center,
                                             self.radius)
        if intersection is not None:
            avoid = self.avoid_vector(intersection)
            return {'intersection': intersection,
                    'avoid': avoid
                    }
        else:
            return None

    def collide_with_circle(self, circle_coords, circle_radius):
        intersection = circle_circle_collision(circle_coords,
                                               circle_radius,
                                               self.center,
                                               self.radius)
        if intersection is not None:
            avoid = self.avoid_vector(intersection)
            return {'intersection': intersection,
                    'avoid': avoid
                    }
        else:
            return None

