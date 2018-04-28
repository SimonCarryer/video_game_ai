from brains.eyes import Eyes, EyeBeam
from screen_objects.wall import Wall
from screen_objects.boy import Boy
import numpy as np


def test_eyes_see_collision():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    coords = np.array((1.0, 3.0))
    vector = np.array((1.0, 0.0))
    collision = eyes.look_for_collisions(coords, vector, 0, 'abc', [wall])
    assert (collision['avoid'] == [0, -1]).all()
    assert (collision['intersection'] == [2, 3]).all()


def test_eyes_see_screen_object():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    coords = np.array((1.0, 3.0))
    eyes_see = eyes.look_at_object(coords, 'abc', wall, [wall])
    assert (eyes_see['intersection'] == [2, 3.5]).all()


def test_eyes_see_boy():
    eyes = Eyes()
    boy = Boy(np.array((2.0, 2.0)), np.array((0.0, 0.0)), 'tootling boy')
    coords = np.array((100.0, 100.0))
    eyes_see = eyes.look_at_object(coords, 'abc', boy, [boy])
    assert eyes_see['intersection'] is not None


def test_eyes_see_screen_object_behind():
    eyes = Eyes()
    wall = Wall(np.array((0.0, 2.0)), np.array((0.0, 5.0)))
    coords = np.array((1.0, 3.0))
    eyes_see = eyes.look_at_object(coords, 'abc', wall, [wall])
    assert (eyes_see['intersection'] == [0.0, 3.5]).all()


def test_eyes_see_unobstructed_screen_object():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    other_wall = Wall(np.array((3.0, 2.0)), np.array((3.0, 5.0)))
    coords = np.array((1.0, 3.0))
    eyes_see = eyes.look_at_object(coords, 'abc', wall, [wall, other_wall])
    assert (eyes_see['intersection'] == [2, 3.5]).all()


def test_eyes_dont_see_obstructed_screen_object():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    other_wall = Wall(np.array((3.0, 2.0)), np.array((3.0, 5.0)))
    coords = np.array((1.0, 3.0))
    eyes_see = eyes.look_at_object(coords, 'abc', other_wall, [wall, other_wall])
    assert eyes_see is None


def test_eyes_see_all_visible_objects():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    other_wall = Wall(np.array((3.0, 2.0)), np.array((3.0, 5.0)))
    third_wall = Wall(np.array((0.5, 2.0)), np.array((0.5, 5.0)))
    coords = np.array((1.0, 3.0))
    visible = eyes.visible_objects(coords, 'abc', [wall, other_wall, third_wall])
    assert len(visible) == 2


def test_eyes_see_all_visible_objects_again():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    other_wall = Wall(np.array((3.0, 2.0)), np.array((3.0, 5.0)))
    third_wall = Wall(np.array((0.5, 2.0)), np.array((0.5, 5.0)))
    boy = Boy(np.array((100.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    coords = np.array((10.0, 30.0))
    visible = eyes.visible_objects(coords, 'abc', [wall, other_wall, third_wall])
    assert len(visible) == 3
