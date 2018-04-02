from util.helpers import *


class Hindbrain:
    def __init__(self):
        self.arrive_distance = 5.0

    def calculate_vector_to_target(self, current_position, current_velocity, target_position):
        anticipated_position = current_position + current_velocity
        arrival_factor = self.arrive_factor(anticipated_position,
                                            target_position)
        return normalise_vector(target_position - anticipated_position) * arrival_factor

    def arrive_factor(self, current_position, target_position):
        current_distance_to_target = distance_between_points(current_position, 
                                                        target_position)
        if current_distance_to_target < self.arrive_distance:
            return current_distance_to_target/self.arrive_distance
        else: 
            return 1.0
