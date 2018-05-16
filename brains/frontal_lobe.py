from pathfinding.grid import BackgroundGrid
from util.helpers import unobstructed_edges, find_closest_point_index
import numpy as np


class FrontalLobe:
    def __init__(self, arena_width, arena_height, grid_spacing):
        self.grid = BackgroundGrid(arena_width, arena_height, grid_spacing)

    def walls_vector_from_game_objects(self, list_of_game_objects):
        walls = [game_object for game_object in list_of_game_objects if game_object.image['kind'] == 'wall']
        return np.array([[wall.start[0], wall.start[1], wall.end[0], wall.end[1]] for wall in walls])

    def populate_grid(self, list_of_game_objects):
        walls = self.walls_vector_from_game_objects(list_of_game_objects)
        self.grid.calculate_edges(walls)

    def direct_path_to_goal(self, current_position, goal, list_of_game_objects):
        walls_vector = self.walls_vector_from_game_objects(list_of_game_objects)
        if len(walls_vector) == 0:
            return True
        goal_edge = np.array([[current_position[0], current_position[1], goal[0], goal[1]]])
        return unobstructed_edges(goal_edge, walls_vector)

    def closest_node(self, position):
        nodes = self.grid.graph.nodes()
        closest_index = find_closest_point_index(position, np.array(nodes))
        return nodes[closest_index]

    def pathfind_goal(self, current_position, goal):
        current_node = self.closest_node(current_position)
        goal_node = self.closest_node(goal)
        path = self.grid.pathfind(current_node, goal_node)
        if path is not None and len(path) > 1:
            return np.array(path[1])
        if path is not None and len(path) == 1:
            return np.array(path[0])
        else:
            return None
        
    def pathfind(self, current_position, goal, list_of_game_objects):
        if self.direct_path_to_goal(current_position, goal, list_of_game_objects):
            goal = goal
        else:
            goal = self.pathfind_goal(current_position, goal)
        return goal

        