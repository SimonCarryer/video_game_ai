from .grid import BackgroundGrid
from util.helpers import *
import numpy as np


class GoalGetter(object):
    def __init__(self, body, eyes):
        self.body = body
        self.eyes = eyes

    def update(self):
        pass

    def goal_position(self, action):
        goal_position = None
        if action.target() == 'mouse pointer':
            goal_position = self.eyes.get_mouse_position()
        elif action.target() is None:
            goal_position = action.goal()
        else:
            goal = self.eyes.look_for_object(self.body.coords,
                                             action.target()
                                             )
            if goal is not None:
                goal_position = goal.coords()
        return goal_position


class PathFindingGoalGetter(GoalGetter):
    def __init__(self, body, eyes, memory):
        self.body = body
        self.eyes = eyes
        self.memory = memory

    def intitialise_grid(self, arena, grid_spacing, walls=[]):
        self.grid = BackgroundGrid(arena.w, arena.h, grid_spacing)
        walls = walls_vector_from_game_objects(walls)
        self.grid.calculate_edges(walls)

    def goal_position(self, action):
        goal_position = super(PathFindingGoalGetter, self).goal_position(action)
        if goal_position is not None and not self.eyes.direct_path_to_goal(self.body.coords, goal_position):
            goal_position = self.pathfind_goal(goal_position)
        return goal_position

    def update(self):
        walls = self.memory.known_walls
        self.update_grid(walls)
        
    def populate_grid(self, list_of_game_objects):
        walls = walls_vector_from_game_objects(list_of_game_objects)
        self.grid.calculate_edges(walls)

    def update_grid(self, list_of_game_objects):
        walls = walls_vector_from_game_objects(list_of_game_objects)
        self.grid.remove_edges(walls)

    def closest_node(self, position):
        nodes = self.grid.graph.nodes()
        closest_index = find_closest_point_index(position, np.array(nodes))
        return nodes[closest_index]

    def pathfind_goal(self, goal):
        current_node = self.closest_node(self.body.coords)
        goal_node = self.closest_node(goal)
        path = self.grid.pathfind(current_node, goal_node)
        if path is not None and len(path) > 1:
            return np.array(path[1])
        if path is not None and len(path) == 1:
            return np.array(path[0])
        else:
            return None


class FastPathFindingGoalGetter(PathFindingGoalGetter):
    def __init__(self, body, eyes, memory):
        super(FastPathFindingGoalGetter, self).__init__(body, eyes, memory)
        self.memory.storage['last_goal'] = np.array([None, None])
        self.memory.storage['last_target_node'] = np.array([None, None])
        self.memory.storage['path'] = []

    def update(self):
        pass

    def intitialise_grid(self, grid):
        self.grid = grid

    def construct_path(self, goal):
        current_node = self.closest_node(self.body.coords)
        goal_node = self.closest_node(goal)
        path = self.grid.pathfind(current_node, goal_node)
        self.memory.storage['path'] = path

    def pathfind_goal(self, goal):
        if (self.memory.storage['last_goal'] == goal).all():
            path = self.memory.storage['path']
            if path is not None and len(path) > 1:
                target_node = np.array(path[1])
            elif path is not None and len(path) == 1:
                target_node = np.array(path[0])
            if distance_between_points(self.body.coords, target_node) < 5:
                self.memory.storage['path'] = path[1:]
        else:
            self.construct_path(goal)
            path = self.memory.storage['path']
            if path is not None and len(path) > 1:
                target_node = np.array(path[1])
            elif path is not None and len(path) == 1:
                target_node = np.array(path[0])
        return target_node