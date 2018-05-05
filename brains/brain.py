from hindbrain import Hindbrain
from util.helpers import *
from eyes import Eyes
from numpy.random import normal
import random


class Brain:
    def __init__(self, image):
        self.hindbrain = Hindbrain()
        self.eyes = Eyes()
        self.parse_behaviour(image.get('behaviour', {}))
        self.self_image = image
        self.wander_value = 0

    def parse_behaviour(self, behaviour_dict):
        self.target = behaviour_dict.get('target')
        self.target_range = behaviour_dict.get('target range')
        if behaviour_dict.get('target behaviour') == 'seek':
            self.target_behviour = self.seek
        elif behaviour_dict.get('target behaviour') == 'flee':
            self.target_behviour = self.flee
        else:
            self.target_behviour = self.wander

    def seek(self,
             target_position,
             current_position,
             current_velocity,
             collision):
        vector_to_target = self.hindbrain.calculate_vector_to_target(current_position,
                                                                     current_velocity,
                                                                     target_position
                                                                     )
        avoid_vector = self.hindbrain.avoid(current_position,
                                            vector_to_target,
                                            collision,
                                            target_position=target_position
                                            )
        arrive_factor = self.hindbrain.arrive_factor(current_position, current_velocity, target_position)
        return normalise_vector(vector_to_target + avoid_vector) * arrive_factor

    def flee(self,
             scary_thing,
             current_position,
             current_velocity,
             collision):
        vector_to_target = self.hindbrain.calculate_vector_to_target(current_position,
                                                                     current_velocity,
                                                                     scary_thing
                                                                     )
        vector = -vector_to_target
        avoid_vector = self.hindbrain.avoid(current_position,
                                            vector,
                                            collision,
                                            target_position=None
                                            )
        return normalise_vector(vector + avoid_vector)

    def wander(self,
               goal,
               current_position,
               current_velocity,
               collision):
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

    def goal_position(self,
                      current_position,
                      list_of_game_objects):
        goal_position = None
        if self.target == 'mouse pointer':
            goal_position = self.eyes.get_mouse_position()
        else:
            goal = self.eyes.look_for_object(current_position,
                                             self.self_image['name'],
                                             self.target_range,
                                             self.target,
                                             list_of_game_objects)
            if goal is not None:
                goal_position = goal['intersection']
        return goal_position

    def get_goal_vector(self,
                        current_position,
                        current_velocity,
                        list_of_game_objects):
        goal = self.goal_position(current_position,
                                  list_of_game_objects)
        collision = self.eyes.look_for_collisions(current_position,
                                                  current_velocity,
                                                  self.self_image['radius'],
                                                  self.self_image['name'],
                                                  list_of_game_objects)
        if goal is not None:
            vector = self.target_behviour(goal,
                                        current_position,
                                        current_velocity,
                                        collision)
        else:
             vector = self.wander(goal,
                                  current_position,
                                  current_velocity,
                                  collision)           
        return vector

