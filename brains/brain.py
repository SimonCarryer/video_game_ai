from hindbrain import Hindbrain
from util.helpers import *
from eyes import Eyes
from numpy.random import normal
from action_planning.actions import *
import numpy as np
import random


class Brain(object):
    def __init__(self, body, image):
        self.body = body
        self.hindbrain = Hindbrain()
        self.eyes = Eyes()
        self.parse_behaviour(image.get('behaviour', {}))
        self.self_image = image
        self.wander_value = 0

    def update(self, list_of_game_objects):
        self.eyes.update(list_of_game_objects)

    def parse_behaviour(self, behaviour_dict):
        self.target = behaviour_dict.get('target')
        self.pathfind = behaviour_dict.get('pathfind', False)
        self.target_range = behaviour_dict.get('target range')
        self.action = Action()
        if behaviour_dict.get('target behaviour') == 'seek':
            self.action = SeekAction(behaviour_dict.get('target'))
        elif behaviour_dict.get('target behaviour') == 'flee':
            self.action = FleeAction(behaviour_dict.get('target'))

    def remember_what_you_see(self, list_of_game_objects):
        visible = self.eyes.visible_objects(self.body.coords, list_of_game_objects)
        self.memory.remember_walls(visible)
        self.frontal_lobe.populate_grid(self.memory.known_walls)

    def seek(self,
             target_position,
             collision):
        vector_to_target = self.hindbrain.calculate_vector_to_target(self.body.coords,
                                                                     self.body.velocity,
                                                                     target_position
                                                                     )
        if not self.pathfind:
            avoid_vector = self.hindbrain.avoid(self.body.coords,
                                                vector_to_target,
                                                collision,
                                                target_position=target_position
                                                )
        else:
            avoid_vector = np.array((0, 0))
        arrive_factor = self.hindbrain.arrive_factor(self.body.coords,
                                                     self.body.velocity,
                                                     target_position)
        return normalise_vector(vector_to_target + avoid_vector) * arrive_factor

    def flee(self,
             scary_thing,
             collision):
        vector_to_target = self.hindbrain.calculate_vector_to_target(self.body.coords,
                                                                     self.body.velocity,
                                                                     scary_thing
                                                                     )
        vector = -vector_to_target
        avoid_vector = self.hindbrain.avoid(self.body.coords,
                                            vector,
                                            collision,
                                            target_position=None
                                            )
        return normalise_vector(vector + avoid_vector)

    def wander(self,
               goal,
               collision):
        if collision is not None:
            vector = self.hindbrain.calculate_vector_to_target(self.body.coords,
                                                               self.body.velocity,
                                                               collision['intersection'])
            return -vector
        change_chance = 0.07
        turn_force = 0.7
        if random.uniform(0, 1) < change_chance:
            self.wander_value = random.choice([-2, -1, 0, 0, 1, 2]) * turn_force
        wander_force = (normalise_vector(perpendicular_vector(self.body.velocity))
                        ) * self.wander_value
        vector = normalise_vector(self.body.velocity + wander_force)
        return vector

    def goal_position(self,
                      list_of_game_objects):
        goal_position = None
        if self.action.target() == 'mouse pointer':
            goal_position = self.eyes.get_mouse_position()
        if self.action.target() is None:
            goal_position = self.action.goal()
        else:
            goal = self.eyes.look_for_object(self.body.coords,
                                             self.target_range,
                                             self.action.target()
                                             )
            if goal is not None:
                goal_position = goal.coords()
        if goal_position is not None and self.pathfind and not self.eyes.direct_path_to_goal(self.body.coords, goal_position):
            goal_position = self.frontal_lobe.pathfind_goal(self.body.coords, goal_position)
        return goal_position

    def get_goal_vector(self,
                        list_of_game_objects):
        goal = self.goal_position(list_of_game_objects)
        collision = self.eyes.look_for_collisions(self.body.coords,
                                                  self.body.velocity,
                                                  self.self_image['radius']
                                                  )
        if goal is not None:
            if self.action.behaviour() == 'seek':
                vector = self.seek(goal, collision)
            elif self.action.behaviour() == 'flee':
                vector = self.flee(goal, collision)
        else:
             vector = self.wander(goal,
                                  collision)
        return vector

