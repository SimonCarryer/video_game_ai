from hindbrain import Hindbrain
from eyes import Eyes


class Brain:
    def __init__(self):
        self.hindbrain = Hindbrain()
        self.eyes = Eyes()

    def follow_mouse_pointer(self, current_position, current_velocity):
        mouse_position = self.eyes.get_mouse_position()
        vector = self.hindbrain.calculate_vector_to_target(current_position,
                                                           current_velocity,
                                                           mouse_position)
        return vector

    def get_goal_vector(self, current_position, current_velocity):
        return self.follow_mouse_pointer(current_position, current_velocity)
