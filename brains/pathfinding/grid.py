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
        weights = []
        for x in range(self.grid_spacing/2, (self.grid_x * self.grid_spacing), self.grid_spacing):
            for y in range(self.grid_spacing/2, (self.grid_y * self.grid_spacing), self.grid_spacing):
                if x >= self.grid_spacing:
                    edges.append((x, y, x-self.grid_spacing, y))
                    weights.append(1)
                if y >= self.grid_spacing:
                    edges.append((x, y, x, y-self.grid_spacing))
                    weights.append(1)
                if x >= self.grid_spacing and y >= self.grid_spacing:
                    edges.append((x, y, x-self.grid_spacing, y-self.grid_spacing))
                    weights.append(1.2)
                if y + self.grid_spacing <= (self.grid_y*self.grid_spacing) and x >= self.grid_spacing:
                    edges.append((x, y, x-self.grid_spacing, y+self.grid_spacing))
                    weights.append(1.2)
        return np.array(edges)

    def weights(self):
        weights = []
        for x in range(self.grid_spacing/2, (self.grid_x * self.grid_spacing), self.grid_spacing):
            for y in range(self.grid_spacing/2, (self.grid_y * self.grid_spacing), self.grid_spacing):
                if x >= self.grid_spacing:
                    weights.append(1)
                if y >= self.grid_spacing:
                    weights.append(1)
                if x >= self.grid_spacing and y >= self.grid_spacing:
                    weights.append(1.2)
                if y + self.grid_spacing <= (self.grid_y*self.grid_spacing) and x >= self.grid_spacing:
                    weights.append(1.2)
        return np.array(weights)

    def calculate_edges(self, wall_vector):
        edges = self.edges()
        weights = self.weights()
        if len(wall_vector) > 0:
            unobstructed_indices = unobstructed_edges(edges, wall_vector)
            final_edges = [((s_x, s_y), (e_x, e_y)) for s_x, s_y, e_x, e_y in edges[unobstructed_indices]]
            weights = weights[unobstructed_indices]
        else:
            final_edges = [((s_x, s_y), (e_x, e_y)) for s_x, s_y, e_x, e_y in edges]
        for nodes, weight in zip(final_edges, weights):
            self.graph.add_edge(nodes[0], nodes[1], weight=weight)

    def remove_edges(self, wall_vector):
        edges = np.array([(s_x, s_y, e_x, e_y) for (s_x, s_y), (e_x, e_y) in self.graph.edges()])
        unobstructed_indices = unobstructed_edges(edges, wall_vector)
        for edge in edges[~unobstructed_indices]:
            self.graph.remove_edge((edge[0], edge[1]), (edge[2], edge[3]))

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