from pathfinding.grid import BackgroundGrid
from util.helpers import unobstructed_edges, find_closest_point_index, walls_vector_from_game_objects
import numpy as np


class FrontalLobe:
    def __init__(self, arena_width, arena_height, grid_spacing):
        self.grid = BackgroundGrid(arena_width, arena_height, grid_spacing)

    def populate_grid(self, list_of_game_objects):
        walls = walls_vector_from_game_objects(list_of_game_objects)
        self.grid.calculate_edges(walls)

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
        