from hindbrain import Hindbrain
from util.helpers import *
from eyes import Eyes
from numpy.random import normal
import random


class SelfImage:
    def __init__(self, body_size, name):
        self.body_size = body_size
        self.name = name


class Brain:
    def __init__(self, body_size, name):
        self.hindbrain = Hindbrain()
        self.eyes = Eyes()
        self.self_image = SelfImage(body_size, name)
        self.wander_value = 0

    def wander(self,
               current_position,
               current_velocity,
               list_of_game_objects):
        collision = self.eyes.look_for_collisions(current_position,
                                                  current_velocity,
                                                  self.self_image.body_size,
                                                  self.self_image.name,
                                                  list_of_game_objects)
        if collision is not None:
            vector = self.hindbrain.calculate_vector_to_target(current_position,
                                                           current_velocity,
                                                           collision['intersection'])
            return -vector
        change_chance = 0.07
        turn_force = 0.7
        if random.uniform(0, 1) < change_chance:
            self.wander_value = random.choice([-2, -1, 0, 0, 1, 2]) * turn_force
        wander_force = (normalise_vector(perpendicular_vector(current_velocity))
                        ) * self.wander_value
        vector = normalise_vector(current_velocity + wander_force)
        return vector/4

    def follow_mouse_pointer(self,
                             current_position,
                             current_velocity,
                             list_of_game_objects):
        mouse_position = self.eyes.get_mouse_position()
        collision = self.eyes.look_for_collisions(current_position,
                                                  current_velocity,
                                                  self.self_image.body_size,
                                                  self.self_image.name,
                                                  list_of_game_objects)
        vector = self.hindbrain.calculate_vector_to_target(current_position,
                                                           current_velocity,
                                                           mouse_position)
        return self.hindbrain.avoid(current_position,
                                    vector,
                                    collision,
                                    target_position=mouse_position
                                    )

    def get_goal_vector(self, 
                        current_position,
                        current_velocity,
                        list_of_game_objects):
        return self.wander(current_position,
                           current_velocity,
                           list_of_game_objects)
