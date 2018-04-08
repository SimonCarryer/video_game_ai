import numpy as np
from util.helpers import *


class ObstructingLine:
    def __init__(self, start, end):
        self.start = np.array(start)
        self.end = np.array(end)
        self.normal_start, self.normal_end = line_normal(self.start, self.end)
        self.center = center_of_line(self.start, self.end)
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
        intersection = circle_line_collision(self.start, 
                                             self.end, 
                                             circle_coords,
                                             circle_radius)
        if intersection is not None:
            avoid = self.avoid_vector(circle_coords)
            return {'intersection': intersection,
                    'avoid': avoid
                    }
        else:
            return None

    def collide_with_line(self, line_start, line_end):
        if check_for_line_intersection(self.start, self.end, line_start, line_end):
            intersection = find_intersecting_point(self.start, self.end, line_start, line_end)
            avoid = self.avoid_vector(intersection)
            return {'intersection': intersection,
                    'avoid': avoid
                    }
        else:
            return None

    def avoid_vector(self, collision_point):
        return normalise_vector(self.center - collision_point)
