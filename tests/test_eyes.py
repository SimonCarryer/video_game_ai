from brains.eyes import Eyes, EyeBeam
from screen_objects.wall import Wall
from screen_objects.boy import Boy
import numpy as np

import inspect

def test_eyes_see_collision():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    coords = np.array((1.0, 3.0))
    vector = np.array((1.0, 0.0))
    collision = eyes.look_for_collisions(coords, vector, 0, [wall])
    assert (collision['avoid'] == [0, -1]).all()
    assert (collision['intersection'] == [2, 3]).all()


def test_eyes_see_screen_object():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    coords = np.array((1.0, 3.0))
    eyes_see = eyes.look_at_object(coords, wall, [wall])
    assert (eyes_see['intersection'] == [2, 3.5]).all()


def test_eyes_see_boy():
    eyes = Eyes()
    boy = Boy(np.array((2.0, 2.0)), np.array((0.0, 0.0)), 'tootling boy')
    coords = np.array((100.0, 100.0))
    eyes_see = eyes.look_at_object(coords, boy, [boy])
    assert eyes_see['intersection'] is not None


def test_eyes_see_screen_object_behind():
    eyes = Eyes()
    wall = Wall(np.array((0.0, 2.0)), np.array((0.0, 5.0)))
    coords = np.array((1.0, 3.0))
    eyes_see = eyes.look_at_object(coords, wall, [wall])
    assert (eyes_see['intersection'] == [0.0, 3.5]).all()


def test_eyes_see_unobstructed_screen_object():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    other_wall = Wall(np.array((3.0, 2.0)), np.array((3.0, 5.0)))
    coords = np.array((1.0, 3.0))
    eyes_see = eyes.look_at_object(coords, wall, [wall, other_wall])
    assert (eyes_see['intersection'] == [2, 3.5]).all()


def test_eyes_dont_see_obstructed_screen_object():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    other_wall = Wall(np.array((3.0, 2.0)), np.array((3.0, 5.0)))
    coords = np.array((1.0, 3.0))
    eyes_see = eyes.look_at_object(coords, other_wall, [wall, other_wall])
    assert eyes_see is None


def test_eyes_see_all_visible_objects():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    other_wall = Wall(np.array((3.0, 2.0)), np.array((3.0, 5.0)))
    third_wall = Wall(np.array((0.5, 2.0)), np.array((0.5, 5.0)))
    coords = np.array((1.0, 3.0))
    visible = eyes.visible_objects(coords, [wall, other_wall, third_wall])
    assert len(visible) == 2


def test_eyes_see_all_visible_objects_again():
    eyes = Eyes()
    wall = Wall(np.array((2.0, 2.0)), np.array((2.0, 5.0)))
    other_wall = Wall(np.array((3.0, 2.0)), np.array((3.0, 5.0)))
    third_wall = Wall(np.array((0.5, 2.0)), np.array((0.5, 5.0)))
    boy = Boy(np.array((100.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    coords = np.array((10.0, 30.0))
    visible = eyes.visible_objects(coords, [wall, other_wall, third_wall])
    assert len(visible) == 3


def test_looking_for_something():
    eyes = Eyes()
    boy = Boy(np.array((100.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    coords = np.array((10.0, 30.0))
    seen = eyes.look_for_object(coords, 200, {}, [boy])
    assert seen['image']['kind'] == 'boy'


def test_looking_for_something_in_particular():
    eyes = Eyes()
    boy = Boy(np.array((100.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    other_boy = Boy(np.array((120.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    other_boy.image['eyes'] = 'kind'
    coords = np.array((10.0, 30.0))
    seen = eyes.look_for_object(coords, 200, {'eyes': 'kind'}, [boy, other_boy])
    assert seen['image']['eyes'] == 'kind'


def test_looking_for_closest_thing():
    eyes = Eyes()
    boy = Boy(np.array((100.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    other_boy = Boy(np.array((120.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    coords = np.array((10.0, 30.0))
    seen = eyes.look_for_object(coords, 200, {}, [boy, other_boy])
    assert (seen['intersection'] == (100.0, 100.0)).all()


def test_looking_for_hidden_thing():
    eyes = Eyes()
    boy = Boy(np.array((100.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    other_boy = Boy(np.array((120.0, 100.0)), np.array((0.0, 0.0)), 'tootling boy')
    wall = Wall(np.array((20.0, 2.0)), np.array((20.0, 150.0)))
    coords = np.array((10.0, 30.0))
    seen = eyes.look_for_object(coords, 200, {'kind': 'tootling boy'}, [boy, other_boy, wall])
    assert seen is None
