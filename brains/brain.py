from hindbrain import Hindbrain
from util.helpers import *
from eyes import Eyes
from numpy.random import normal
from frontal_lobe import FrontalLobe
from memory import Memory
import numpy as np
import random


class Brain:
    def __init__(self, image):
        self.hindbrain = Hindbrain()
        self.eyes = Eyes()
        self.parse_behaviour(image.get('behaviour', {}))
        self.self_image = image
        self.wander_value = 0
        self.update = self.dumb_update

    def dumb_update(self, current_position, list_of_game_objects):
        pass

    def smart_update(self, current_position, list_of_game_objects):
        visible = self.eyes.visible_objects(current_position, list_of_game_objects)
        self.memory.remember_walls(visible)
        self.frontal_lobe.update_grid(self.memory.known_walls)

    def initialise_frontal_lobe(self, arena_height, arena_width, grid_spacing, list_of_game_objects):
        self.update = self.smart_update
        self.memory = Memory()
        self.frontal_lobe = FrontalLobe(arena_height, arena_width, grid_spacing)
        self.frontal_lobe.populate_grid(list_of_game_objects)

    def parse_behaviour(self, behaviour_dict):
        self.target = behaviour_dict.get('target')
        self.pathfind = behaviour_dict.get('pathfind', False)
        self.target_range = behaviour_dict.get('target range')
        if behaviour_dict.get('target behaviour') == 'seek':
            self.target_behaviour = self.seek
        elif behaviour_dict.get('target behaviour') == 'flee':
            self.target_behaviour = self.flee
        else:
            self.target_behaviour = self.wander

    def remember_what_you_see(self, current_position, list_of_game_objects):
        visible = self.eyes.visible_objects(current_position, list_of_game_objects)
        self.memory.remember_walls(visible)
        self.frontal_lobe.populate_grid(self.memory.known_walls)

    def seek(self,
             target_position,
             current_position,
             current_velocity,
             collision):
        vector_to_target = self.hindbrain.calculate_vector_to_target(current_position,
                                                                     current_velocity,
                                                                     target_position
                                                                     )
        if not self.pathfind:
            avoid_vector = self.hindbrain.avoid(current_position,
                                                vector_to_target,
                                                collision,
                                                target_position=target_position
                                                )
        else:
            avoid_vector = np.array((0, 0))
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
        if self.target is None:
            goal_position = None
        else:
            goal = self.eyes.look_for_object(current_position,
                                             self.target_range,
                                             self.target,
                                             list_of_game_objects)
            if goal is not None:
                goal_position = goal.coords()
        if goal_position is not None and self.pathfind and not self.eyes.direct_path_to_goal(current_position, goal_position, list_of_game_objects):
            goal_position = self.frontal_lobe.pathfind_goal(current_position, goal_position)
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
                                                  list_of_game_objects)
        if goal is not None:
            vector = self.target_behaviour(goal,
                                        current_position,
                                        current_velocity,
                                        collision)
        else:
             vector = self.wander(goal,
                                  current_position,
                                  current_velocity,
                                  collision)           
        return vector

