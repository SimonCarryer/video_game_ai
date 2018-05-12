import networkx as nx
import numpy as np
import pygame
from util.helpers import check_for_line_intersection
from physics.colliding_object import Colliding


class BackgroundGrid():
    def __init__(self, arena_w, arena_h, grid_spacing):
        self.grid_spacing = grid_spacing
        self.grid_x = int(arena_w/self.grid_spacing)
        self.grid_y = int(arena_h/self.grid_spacing)
        self.graph = nx.Graph()
        self.nodecolour = (100, 0, 0)
        self.edgecolour = (38, 75, 0)

    def populate_graph(self, list_of_game_objects):
        walls = [game_object for game_object in list_of_game_objects if game_object.image['kind'] == 'wall']
        self.graph = nx.Graph()
        self.graph.add_edges_from(edges, weight=1)
        self.graph.add_edges_from(edges, weight=1.2)

    def walls_to_vector(self, list_of_walls):
        return np.array([[wall.start[0], wall.start[1], wall.end[0], wall.end[1]] for wall in list_of_walls])

    def edges(self):
        edges = []
        for x in range(self.grid_spacing/2, (self.grid_x * self.grid_spacing), self.grid_spacing):
            for y in range(self.grid_spacing/2, (self.grid_y * self.grid_spacing), self.grid_spacing):
                edges.append((x, y, x-self.grid_spacing, y)) if x >= self.grid_spacing else None
                edges.append((x, y, x, y-self.grid_spacing)) if y >= self.grid_spacing else None
                edges.append((x, y, x-self.grid_spacing, y-self.grid_spacing)) if x >= self.grid_spacing and y >= self.grid_spacing else None
                edges.append((x, y, x-self.grid_spacing, y+self.grid_spacing)) if y + self.grid_spacing <= (self.grid_y*self.grid_spacing) and x >= self.grid_spacing else None
        return np.array(edges)

    def unobstructed_edges(self, edges_vector, list_of_walls):
        wall_vector = self.walls_to_vector(list_of_walls)
        walls_product = np.tile(np.transpose(wall_vector), len(edges_vector))
        edges_product = np.transpose(np.repeat(edges_vector, len(wall_vector), axis=0))
        a = (edges_product[3] - walls_product[1]) * (edges_product[0] - walls_product[0])\
            > (edges_product[1] - walls_product[1]) * (edges_product[2] - walls_product[0])

        b = (edges_product[3] - walls_product[3]) * (edges_product[0] - walls_product[2])\
            > (edges_product[1] - walls_product[3]) * (edges_product[2] - walls_product[2])

        c = (edges_product[1] - walls_product[1]) * (walls_product[2] - walls_product[0])\
            > (walls_product[3] - walls_product[1]) * (edges_product[0] - walls_product[0])

        d = (edges_product[3] - walls_product[1]) * (walls_product[2] - walls_product[0])\
            > (walls_product[3] - walls_product[1]) * (edges_product[2] - walls_product[0])
        intersections = ~((a != b) & (c != d))
        return np.array([i.all() for i in np.split(intersections, len(edges_vector))])

    def calculate_edges(self, list_of_game_objects):
        walls = [game_object for game_object in list_of_game_objects if game_object.image['kind'] == 'wall']
        edges = self.edges()
        final_edges = [((s_x, s_y), (e_x, e_y)) for s_x, s_y, e_x, e_y in edges[self.unobstructed_edges(edges, walls)]]
        self.graph.add_edges_from(final_edges, weight=1)

    def draw(self, screen):
        for edge in self.graph.edges():
            pygame.draw.line(screen, self.edgecolour, edge[0], edge[1])
        for node in self.graph.nodes():
            pygame.draw.circle(screen, self.nodecolour, node, 3)