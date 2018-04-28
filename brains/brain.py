from hindbrain import Hindbrain
from util.helpers import *
from eyes import Eyes
from numpy.random import normal
import random


class Brain:
    def __init__(self, self_image):
        self.hindbrain = Hindbrain()
        self.eyes = Eyes()
        self.self_image = self_image
        self.wander_value = 0
        behaviour_dict = {
            'wander': self.wander,
            'follow mouse pointer': self.follow_mouse_pointer,
            'follow closest boy': self.follow_closest_boy,
            'run from close boys': self.run_from_close_boys
        }
        self.get_goal_vector = behaviour_dict[self_image['behaviour']]

    def follow_closest_boy(self,
                           current_position,
                           current_velocity,
                           list_of_screen_objects):
        visibles = self.eyes.visible_objects(current_position,
                                             self.self_image['name'],
                                             list_of_screen_objects)
        boy_locations = [visible['intersection'] for visible in visibles if visible.get('image')]
        if len(boy_locations) == 0:
            return self.wander(current_position,
                               current_velocity,
                               list_of_screen_objects)
        goal = find_closest_point(current_position, boy_locations)
        vector = self.hindbrain.calculate_vector_to_target(current_position,
                                                           current_velocity,
                                                           goal)
        return vector

    def run_from_close_boys(self,
                            current_position,
                            current_velocity,
                            list_of_screen_objects):
        visibles = self.eyes.visible_objects(current_position,
                                             self.self_image['name'],
                                             list_of_screen_objects)
        boy_locations = [visible['intersection'] for visible in visibles if visible.get('image')]
        if len(boy_locations) == 0:
            return self.wander(current_position,
                               current_velocity,
                               list_of_screen_objects)
        closest_boy = find_closest_point(current_position, boy_locations)
        distance_to_boy = distance_between_points(current_position, closest_boy)
        if distance_to_boy > 200:
            return self.wander(current_position,
                               current_velocity,
                               list_of_screen_objects)
        vector = -self.hindbrain.calculate_vector_to_target(current_position,
                                                            current_velocity,
                                                            closest_boy)
        return vector

    def wander(self,
               current_position,
               current_velocity,
               list_of_game_objects):
        collision = self.eyes.look_for_collisions(current_position,
                                                  current_velocity,
                                                  self.self_image['radius'],
                                                  self.self_image['name'],
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
        return vector

    def follow_mouse_pointer(self,
                             current_position,
                             current_velocity,
                             list_of_game_objects):
        mouse_position = self.eyes.get_mouse_position()
        collision = self.eyes.look_for_collisions(current_position,
                                                  current_velocity,
                                                  self.self_image['radius'],
                                                  self.self_image['name'],
                                                  list_of_game_objects)
        vector = self.hindbrain.calculate_vector_to_target(current_position,
                                                           current_velocity,
                                                           mouse_position)
        return self.hindbrain.avoid(current_position,
                                    vector,
                                    collision,
                                    target_position=mouse_position
                                    )
