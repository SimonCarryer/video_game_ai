from util.helpers import *


class Hindbrain:
    def __init__(self):
        pass

    def calculate_vector_to_target(self, current_position, target_position):
        return normalise_vector(target_position - current_position)
