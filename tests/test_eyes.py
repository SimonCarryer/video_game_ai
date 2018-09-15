from brains.eyes import Eyes, EyeBeam
from screen_objects.wall import Wall
from screen_objects.boy import Boy
import numpy as np


def test_eyes_see_collision():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    coords = np.array((1.0, 3.0))
    vector = np.array((1.0, 0.0))
    list_of_game_objects = [wall]
    eyes.update(list_of_game_objects)
    collision = eyes.look_for_collisions(coords, vector, 0)
    assert (collision['avoid'] == [0, -1]).all()
    assert (collision['intersection'] == [2, 3]).all()


def test_eyes_see_wall():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    coords = np.array((1.0, 3.0))
    list_of_game_objects = [wall]
    eyes.update(list_of_game_objects)
    eyes_see = eyes.look_at_object(coords, wall)
    assert eyes_see == wall


def test_eyes_see_obstructed_wall():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    other_wall = Wall(np.array((3.0, 2.0)), np.array((3.0, 5.0)))
    coords = np.array((1.0, 3.0))
    list_of_game_objects = [wall, other_wall]
    eyes.update(list_of_game_objects)
    eyes_see = eyes.look_at_object(coords, other_wall)
    assert not eyes_see == other_wall


def test_eyes_see_boy():
    eyes = Eyes()
    boy = Boy(np.array((2.0, 2.0)), np.array((0.0, 0.0)), 'tootling boy')
    coords = np.array((100.0, 100.0))
    list_of_game_objects = [boy]
    eyes.update(list_of_game_objects)
    eyes_see = eyes.look_at_object(coords, boy)
    assert eyes_see is not None


def test_eyes_see_screen_object_behind():
    eyes = Eyes()
    boy = Boy(np.array((0.0, 2.0)), np.array((0.0, 0.0)), 'tootling boy')
    coords = np.array((1.0, 3.0))
    list_of_game_objects = []
    eyes.update(list_of_game_objects)
    eyes_see = eyes.look_at_object(coords, boy)
    assert (eyes_see.coords() == [0.0, 2.0]).all()


def test_eyes_see_unobstructed_screen_object():
    eyes = Eyes()
    boy = Boy(np.array((2.0, 2.0)), np.array((0.0, 0.0)), 'tootling boy')
    other_wall = Wall(np.array((3.0, 2.0)), np.array((3.0, 5.0)))
    coords = np.array((1.0, 3.0))
    list_of_game_objects = [boy, other_wall]
    eyes.update(list_of_game_objects)
    eyes_see = eyes.look_at_object(coords, boy)
    assert (eyes_see.coords() == [2, 2]).all()


def test_eyes_dont_see_obstructed_screen_object():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    boy = Boy(np.array((3.0, 3.0)), np.array((0.0, 0.0)), 'tootling boy')
    coords = np.array((1.0, 3.0))
    list_of_game_objects = [wall, boy]
    eyes.update(list_of_game_objects)
    eyes_see = eyes.look_at_object(coords, boy)
    assert eyes_see is None


def test_eyes_see_all_visible_objects_again():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    other_wall = Wall(np.array((3.0, 2.0)), np.array((3.0, 5.0)))
    third_wall = Wall(np.array((0.5, 2.0)), np.array((0.5, 5.0)))
    boy = Boy(np.array((100.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    coords = np.array((10.0, 30.0))
    list_of_game_objects = [boy, wall, other_wall, third_wall]
    eyes.update(list_of_game_objects)
    visible = eyes.visible_objects(coords)
    assert len(visible) == 4


def test_looking_for_something():
    eyes = Eyes()
    boy = Boy(np.array((100.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    coords = np.array((10.0, 30.0))
    list_of_game_objects = [boy]
    eyes.update(list_of_game_objects)
    seen = eyes.look_for_object(coords, {})
    assert seen.image['kind'] == 'boy'


def test_looking_for_something_in_particular():
    eyes = Eyes()
    boy = Boy(np.array((100.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    other_boy = Boy(np.array((120.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    other_boy.image['eyes'] = 'kind'
    coords = np.array((10.0, 30.0))
    list_of_game_objects = [boy, other_boy]
    eyes.update(list_of_game_objects)
    seen = eyes.look_for_object(coords, {'eyes': 'kind'})
    assert seen.image['eyes'] == 'kind'


def test_looking_for_closest_thing():
    eyes = Eyes()
    boy = Boy(np.array((100.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    other_boy = Boy(np.array((120.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    coords = np.array((10.0, 30.0))
    list_of_game_objects = [boy, other_boy]
    eyes.update(list_of_game_objects)
    seen = eyes.look_for_object(coords, {})
    assert (seen.coords() == (100.0, 100.0)).all()


def test_looking_for_hidden_thing():
    eyes = Eyes()
    boy = Boy(np.array((100.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    other_boy = Boy(np.array((120.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    wall = Wall(np.array((20.0, 2.0)), np.array((20.0, 150.0)))
    coords = np.array((10.0, 30.0))
    list_of_game_objects = [boy, other_boy, wall]
    eyes.update(list_of_game_objects)
    seen = eyes.look_for_object(coords, {'kind': 'tootling boy'})
    assert seen is None


def test_direct_path_to_goal_returns_true_when_no_walls():
    eyes = Eyes()
    current_position = np.array((1.0, 1.0))
    goal = np.array((9.0, 9.0))
    list_of_game_objects = []
    eyes.update(list_of_game_objects)
    assert eyes.direct_path_to_goal(current_position, goal)


def test_direct_path_to_goal_returns_true_when_unobstructed():
    eyes = Eyes()
    current_position = np.array((1.0, 1.0))
    goal = np.array((9.0, 9.0))
    wall = Wall((2, 1), (9, 1))
    list_of_game_objects = [wall]
    eyes.update(list_of_game_objects)
    assert eyes.direct_path_to_goal(current_position, goal)


def test_direct_path_to_goal_returns_false_when_obstructed():
    eyes = Eyes()
    current_position = np.array((1.0, 1.0))
    goal = np.array((9.0, 9.0))
    wall = Wall((1, 9), (9, 1))
    list_of_game_objects = [wall]
    eyes.update(list_of_game_objects)
    assert not eyes.direct_path_to_goal(current_position, goal)


def test_direct_path_to_goal_returns_false_when_obstructed_wth_many_walls():
    eyes = Eyes()
    current_position = np.array((1.0, 1.0))
    goal = np.array((9.0, 9.0))
    wall = Wall((1, 9), (9, 1))
    wall_2 = Wall((2, 9), (10, 2))
    list_of_game_objects = [wall, wall_2]
    eyes.update(list_of_game_objects)
    assert not eyes.direct_path_to_goal(current_position, goal)