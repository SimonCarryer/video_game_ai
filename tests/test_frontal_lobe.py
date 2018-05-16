from brains.frontal_lobe import FrontalLobe
from screen_objects.wall import Wall
import numpy as np


def test_direct_path_to_goal_returns_true_when_no_walls():
    lobe = FrontalLobe(10, 10, 10)
    current_position = np.array((1.0, 1.0))
    goal = np.array((9.0, 9.0))
    list_of_game_objects = []
    assert lobe.direct_path_to_goal(current_position, goal, list_of_game_objects)


def test_direct_path_to_goal_returns_true_when_unobstructed():
    lobe = FrontalLobe(10, 10, 10)
    current_position = np.array((1.0, 1.0))
    goal = np.array((9.0, 9.0))
    wall = Wall((2, 1), (9, 1))
    list_of_game_objects = [wall]
    assert lobe.direct_path_to_goal(current_position, goal, list_of_game_objects)


def test_direct_path_to_goal_returns_false_when_unobstructed():
    lobe = FrontalLobe(10, 10, 10)
    current_position = np.array((1.0, 1.0))
    goal = np.array((9.0, 9.0))
    wall = Wall((1, 9), (9, 1))
    list_of_game_objects = [wall]
    assert not lobe.direct_path_to_goal(current_position, goal, list_of_game_objects)


def test_walls_to_vector():
    lobe = FrontalLobe(100, 100, 20)
    wall = Wall((12, 12), (12, 32))
    wall_2 = Wall((22, 12), (22, 32))
    vector = lobe.walls_vector_from_game_objects([wall, wall_2])
    assert (vector == np.array([[12, 12, 12, 32], [22, 12, 22, 32]])).all()


def test_populate_grid():
    lobe = FrontalLobe(100, 100, 20)
    lobe.populate_grid([])


def test_closest_node():
    lobe = FrontalLobe(100, 100, 20)
    lobe.populate_grid([])
    position = np.array((0, 21))
    assert lobe.closest_node(position) == (10, 30)


def test_pathfind_goal():
    lobe = FrontalLobe(100, 100, 20)
    lobe.populate_grid([])
    position = np.array((0, 21))
    goal = np.array((81, 71))
    assert (lobe.pathfind_goal(position, goal) == (30, 30)).all()

