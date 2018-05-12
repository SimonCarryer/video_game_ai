from brains.pathfinding.grid import BackgroundGrid
from screen_objects.wall import Wall
import numpy as np
import timeit

def test_walls_to_vector():
    grid = BackgroundGrid(100, 100, 20)
    wall = Wall((12, 12), (12, 32))
    wall_2 = Wall((22, 12), (22, 32))
    vector = grid.walls_to_vector([wall, wall_2])
    assert (vector == np.array([[12, 12, 12, 32], [22, 12, 22, 32]])).all()


def test_edges():
    grid = BackgroundGrid(100, 100, 20)
    assert len(grid.edges()) == 72


def test_unobstructed_edges():
    grid = BackgroundGrid(100, 100, 20)
    wall_vector = np.array([[12, 12, 12, 32], [12, 12, 12, 14]])
    assert grid.unobstructed_edges(grid.edges(), wall_vector).sum() == 69


def test_calculate_edges():
    grid = BackgroundGrid(100, 100, 20)
    wall = Wall((12, 12), (12, 32))
    wall2 = Wall((12, 12), (12, 14))
    grid.calculate_edges([wall, wall2])
    assert len(grid.graph.edges()) == 69
    
