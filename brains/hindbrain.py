from util.helpers import *


class Hindbrain:
    def __init__(self):
        self.arrive_distance = 5.0

    def avoid(self,
              current_position,
              vector,
              collision,
              target_position=None
              ):
        if collision:
            # check if target will be reached before hitting wall
            if target_position is not None and find_closest_point_index(current_position, 
                                                                        [collision['intersection'],
                                                                        target_position]) == 0:
                vector = collision['avoid']
            elif target_position is None:
                vector = collision['avoid']
        return vector

    def calculate_vector_to_target(self,
                                   current_position,
                                   current_velocity,
                                   target_position):
        anticipated_position = current_position + current_velocity
        vector = normalise_vector(target_position - anticipated_position)
        return vector

    def arrive_factor(self, current_position, current_velocity, target_position):
        anticipated_position = current_position + current_velocity
        current_distance_to_target = distance_between_points(anticipated_position, 
                                                             target_position)
        if current_distance_to_target < self.arrive_distance:
            return current_distance_to_target/self.arrive_distance
        else: 
            return 1.0
