from screen_objects.item import Item
from brains.eyes import Eyes
from screen_objects.boy import Boy
import numpy as np


def test_item_can_be_seen():
    item = Item((10, 10), (100, 100, 100))
    eyes = Eyes()
    list_of_game_objects = [item]
    eyes.update(list_of_game_objects)
    coords = np.array((0, 0))
    assert len(eyes.visible_objects(coords)) == 1
    assert eyes.look_for_object(coords, {'kind': 'item'}) == item


def test_item_gets_picked_up():
    item = Item((10, 10), (100, 100, 100))
    boy = Boy(np.array((10.0, 10.0)), np.array((0.0, 0.0)), 'tootling boy')
    list_of_game_objects = [boy]
    assert not item.delete
    item.get_picked_up(list_of_game_objects)
    assert item.delete