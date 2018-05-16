from brains.pathfinding.grid import BackgroundGrid
import numpy as np
import timeit


def test_edges():
    grid = BackgroundGrid(100, 100, 20)
    assert len(grid.edges()) == 72


def test_calculate_edges():
    grid = BackgroundGrid(100, 100, 20)
    wall_vector = np.array([[12, 12, 12, 32], [12, 12, 12, 14]])
    grid.calculate_edges(wall_vector)
    assert len(grid.graph.edges()) == 69  # nice


def test_pathfind_returns_path_when_not_obstructed():
    grid = BackgroundGrid(100, 100, 20)
    grid.calculate_edges([])
    start_node = (10, 10)
    goal_node = (90, 90)
    path = grid.pathfind(start_node, goal_node)
    assert path == [(10, 10), (30, 30), (50, 50), (70, 70), (90, 90)]


def test_pathfind_returns_none_when_obstructed():
    grid = BackgroundGrid(100, 100, 20)
    wall_vector = np.array([[30, 0, 30, 100]])
    grid.calculate_edges(wall_vector)
    start_node = (10, 10)
    goal_node = (90, 90)
    path = grid.pathfind(start_node, goal_node)
    assert path is None
