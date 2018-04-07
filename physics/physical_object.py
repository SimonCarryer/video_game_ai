import numpy as np
from util.helpers import *


class ObstructingLine:
    def __init__(self, start, end):
        self.start = np.array(start)
        self.end = np.array(end)
        self.normal_start, self.normal_end = line_normal(self.start, self.end)
        self.collide_type = None

    def collide(self, colliding_object):
        if colliding_object.collide_type == 'circle':
            return self.collide_with_circle(colliding_object.coords,
                                            colliding_object.radius)
        elif colliding_object.collide_type == 'line':
            return self.collide_with_line(colliding_object.start,
                                          colliding_object.end)
        else:
            return None

    def collide_with_circle(self, circle_coords, circle_radius):
        return circle_line_collision(self.start, 
                                     self.end, 
                                     circle_coords,
                                     circle_radius)

    def collide_with_line(self, line_start, line_end):
        if check_for_line_intersection(self.start, self.end, line_start, line_end):
            intersection = find_intersecting_point(self.start, self.end, line_start, line_end)
            avoid_angle = self.avoid_angle(line_start)
            return {'intersection': intersection,
                    'avoid_angle': avoid_angle
            }
        else:
            return None

    def avoid_angle(self, point):
        closest = find_closest_point(point, [self.normal_start, self.normal_end])
        return normalise_vector(closest)
