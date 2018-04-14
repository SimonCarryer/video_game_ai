from hindbrain import Hindbrain
from eyes import Eyes


class SelfImage:
    def __init__(self, body_size):
        self.body_size = body_size


class Brain:
    def __init__(self, body_size):
        self.hindbrain = Hindbrain()
        self.eyes = Eyes()
        self.self_image = SelfImage(body_size)

    def follow_mouse_pointer(self,
                             current_position,
                             current_velocity,
                             list_of_game_objects):
        mouse_position = self.eyes.get_mouse_position()
        collision = self.eyes.look_for_collisions(current_position,
                                                  current_velocity,
                                                  self.self_image.body_size,
                                                  list_of_game_objects)
        vector = self.hindbrain.calculate_vector_to_target(current_position,
                                                           current_velocity,
                                                           mouse_position,
                                                           collision=collision)
        return vector

    def get_goal_vector(self, 
                        current_position,
                        current_velocity,
                        list_of_game_objects):
        return self.follow_mouse_pointer(current_position,
                                         current_velocity,
                                         list_of_game_objects)
