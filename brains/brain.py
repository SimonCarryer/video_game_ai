from hindbrain import Hindbrain
from util.helpers import *
from eyes import Eyes
from numpy.random import normal
from action_planning.actions import *
from action_planning.action_planner import ActionGetter, ActionPlanner
from pathfinding.pathfinder import GoalGetter, PathFindingGoalGetter, FastPathFindingGoalGetter
from .memory import DumbMemory, Memory
import numpy as np
import random


class Brain(object):
    def __init__(self, body, image):
        self.body = body
        self.hindbrain = Hindbrain()
        view_distance = image.get('behaviour', {}).get('target range', 200)
        self.eyes = Eyes(view_distance=view_distance)
        self.self_image = image
        self.parse_behaviour(image.get('behaviour', {}))
        self.wander_value = 0

    def update(self, list_of_game_objects):
        self.eyes.update(list_of_game_objects)
        self.memory.update()
        self.action_getter.update()
        self.goal_getter.update()
        self.action = self.action_getter.action
        
    def parse_behaviour(self, behaviour_dict):
        if behaviour_dict.get('goap', False):
            self.action_getter = ActionPlanner(self.self_image, self.eyes, self.body)
        else:
            self.action_getter = ActionGetter(self.self_image, self.eyes, self.body)
        if behaviour_dict.get('pathfind', False):
            self.memory = Memory(self.body, self.eyes)
            self.goal_getter = PathFindingGoalGetter(self.body, self.eyes, self.memory)
        elif behaviour_dict.get('fast pathfind', False):
            self.memory = DumbMemory(self.body, self.eyes)
            self.goal_getter = FastPathFindingGoalGetter(self.body, self.eyes, self.memory)
        else:
            self.memory = DumbMemory(self.body, self.eyes)
            self.goal_getter = GoalGetter(self.body, self.eyes)
        self.target = behaviour_dict.get('target')
        self.target_range = behaviour_dict.get('target range')

    def seek(self,
             target_position,
             collision):
        vector_to_target = self.hindbrain.calculate_vector_to_target(self.body.coords,
                                                                     self.body.velocity,
                                                                     target_position
                                                                     )
        avoid_vector = self.hindbrain.avoid(self.body.coords,
                                                vector_to_target,
                                                collision,
                                                target_position=target_position
                                                )
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
        if vector.sum() == 0:
            vector = np.array((1, 0))
        return vector

    def stop(self, goal, collision):
        return self.hindbrain.stop(self.body.coods, self.body.velocity)

    def get_goal_vector(self,
                        list_of_game_objects):
        goal = self.goal_getter.goal_position(self.action)
        collision = self.eyes.look_for_collisions(self.body.coords,
                                                  self.body.velocity,
                                                  self.self_image['radius']
                                                  )
        if goal is not None:
            if self.action.behaviour() == 'seek':
                vector = self.seek(goal, collision)
            elif self.action.behaviour() == 'flee':
                vector = self.flee(goal, collision)
            elif self.action.behaviour() == 'stop':
                vector = self.stop(goal, collision)
        else:
            vector = self.wander(goal,
                                 collision)
        return vector

