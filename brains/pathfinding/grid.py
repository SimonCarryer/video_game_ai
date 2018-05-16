import networkx as nx
import numpy as np
import pygame
from util.helpers import *
from physics.colliding_object import Colliding


class BackgroundGrid():
    def __init__(self, arena_w, arena_h, grid_spacing):
        self.grid_spacing = grid_spacing
        self.grid_x = int(arena_w/self.grid_spacing)
        self.grid_y = int(arena_h/self.grid_spacing)
        self.graph = nx.Graph()
        self.nodecolour = (100, 0, 0)
        self.edgecolour = (38, 75, 0)

    def edges(self):
        edges = []
        for x in range(self.grid_spacing/2, (self.grid_x * self.grid_spacing), self.grid_spacing):
            for y in range(self.grid_spacing/2, (self.grid_y * self.grid_spacing), self.grid_spacing):
                edges.append((x, y, x-self.grid_spacing, y)) if x >= self.grid_spacing else None
                edges.append((x, y, x, y-self.grid_spacing)) if y >= self.grid_spacing else None
                edges.append((x, y, x-self.grid_spacing, y-self.grid_spacing)) if x >= self.grid_spacing and y >= self.grid_spacing else None
                edges.append((x, y, x-self.grid_spacing, y+self.grid_spacing)) if y + self.grid_spacing <= (self.grid_y*self.grid_spacing) and x >= self.grid_spacing else None
        return np.array(edges)

    def calculate_edges(self, wall_vector):
        edges = self.edges()
        if len(wall_vector) > 0:
            final_edges = [((s_x, s_y), (e_x, e_y)) for s_x, s_y, e_x, e_y in edges[unobstructed_edges(edges, wall_vector)]]
        else:
            final_edges = [((s_x, s_y), (e_x, e_y)) for s_x, s_y, e_x, e_y in edges]
        self.graph.add_edges_from(final_edges, weight=1)

    def closest_node(self, point):
        nodes = np.array(self.graph.nodes())
        closest_index = find_closest_point_index(point, nodes)
        return self.graph.nodes()[closest_index]

    def pathfind(self, start_node, goal_node):
        try:
            path = nx.astar_path(self.graph, start_node, goal_node)
        except (nx.NetworkXNoPath):
            path = None
        return path

    def draw(self, screen):
        for edge in self.graph.edges():
            pygame.draw.line(screen, self.edgecolour, edge[0], edge[1])
        for node in self.graph.nodes():
            pygame.draw.circle(screen, self.nodecolour, node, 3)