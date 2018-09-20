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


def test_pick_up_interaction_with_states():
    item = Item((20, 10), (100, 100, 100))
    boy = Boy(np.array((0.0, 10.0)), np.array((0.0, 0.0)), 'customer')
    list_of_game_objects = [item, boy]
    for i in range(20):
        boy.body.move(list_of_game_objects, np.array([-1, 0]))
        boy.brain.eyes.update(list_of_game_objects)
        boy.brain.action_getter.interpreter.update()
        assert boy.brain.action_getter.interpreter.state['got_item'] == item.delete
        if item.delete:
            list_of_game_objects = [boy]