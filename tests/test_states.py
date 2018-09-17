from brains.action_planning.states import *
from brains.eyes import Eyes
from screen_objects.boy import Boy
from mocks.mock_body_parts import *
from screen_objects.item import Item
import numpy as np


def test_base_state_class():
    eyes = MockEyes()
    body = MockBody()
    state = State('test_state', body, eyes)
    assert not state.is_fulfilled()
    assert not state.status()
    state.fulfilled = True
    assert state.is_fulfilled()
    assert state.status()


def test_location_state():
    eyes = MockEyes()
    body = MockBody()
    rect = np.array([[0, 0], [100, 100]])
    state = LocationState('test_state', body, eyes, rect)
    assert state.is_fulfilled()
    assert state.status()
    rect = np.array([[100, 100], [200, 200]])
    state = LocationState('test_state', body, eyes, rect)
    assert not state.is_fulfilled()
    assert not state.status()
    state.body.coords = np.array([150, 150])
    assert state.is_fulfilled()
    assert state.status()


def test_sticky_location_state():
    eyes = MockEyes()
    body = MockBody()
    rect = np.array([[100, 100], [200, 200]])
    state = LocationState('test_state', body, eyes, rect)
    assert not state.is_fulfilled()
    assert not state.status()
    body.coords = [150, 150]
    assert state.is_fulfilled()
    assert state.status()
    body.coords = [50, 50]
    assert not state.is_fulfilled()
    assert state.status()


def test_point_state():
    eyes = MockEyes()
    body = MockBody()
    point = np.array([0, 0])
    state = AtPointState('test_state', body, eyes, point)
    assert not state.is_fulfilled()
    assert not state.status()
    body.coords = [2, 2]
    assert state.is_fulfilled()
    assert state.status()


def test_object_visible_state():
    eyes = Eyes()
    body = MockBody()
    boy = Boy(np.array((2.0, 2.0)), np.array((0.0, 0.0)), 'tootling boy')
    state = SeeObjectState('test_state', body, eyes, {'colour': (0, 0, 220)})
    assert not state.is_fulfilled()
    eyes.update([boy])
    assert state.is_fulfilled()
    # out of distance
    other_boy = Boy(np.array((200.0, 200.0)), np.array((0.0, 0.0)), 'tootling boy')
    eyes.update([other_boy])
    assert not state.is_fulfilled()
    # wrong kind
    third_boy = Boy(np.array((120.0, 120.0)), np.array((0.0, 0.0)), 'friendly boy')
    eyes.update([third_boy])
    assert not state.is_fulfilled()


def test_object_in_location_state():
    eyes = Eyes()
    body = MockBody()
    rect = np.array([[0, 0], [10, 10]])
    boy = Boy(np.array((2.0, 2.0)), np.array((0.0, 0.0)), 'tootling boy')
    state = ObjectInLocationState('test_state', body, eyes, rect, {'colour': (0, 0, 220)})
    assert not state.is_fulfilled()
    eyes.update([boy])
    assert state.is_fulfilled()
    other_boy = Boy(np.array((12.0, 2.0)), np.array((0.0, 0.0)), 'tootling boy')
    eyes.update([other_boy])
    assert not state.is_fulfilled()


def test_state_with_requirements():
    eyes = MockEyes()
    body = MockBody()
    global_state = {'test_state2': False}
    requirements = {'test_state2': True}
    state = State('test_state', body, eyes, state=global_state, requirements={}, sticky=False)
    state.fulfilled = True
    assert state.requirements_met()
    assert state.status()
    state = State('test_state', body, eyes, state=global_state, requirements=requirements, sticky=False)
    state.fulfilled = True
    assert not state.status()
    state = State('test_state', body, eyes, state=global_state, requirements=requirements)
    state.fulfilled = True
    global_state['test_state2'] = True
    assert state.status()


def test_pick_up_success_with_two_boys():
    item = Item((20, 10), (100, 100, 100))
    other_item = Item((0, 0), (100, 100, 100))
    boy = Boy(np.array((0.0, 10.0)), np.array((0.0, 0.0)), 'customer')
    other_boy = Boy(np.array((0.0, 0.0)), np.array((0.0, 0.0)), 'customer')
    list_of_game_objects = [item, other_item, boy, other_boy]
    print id(boy.brain.interpreter.state)
    boy.brain.interpreter.state['got_item'] == True
    print id(other_boy.brain.interpreter.state)
    print other_boy.brain.interpreter.state['got_item']

    # for i in range(20):
    #     other_boy.brain.eyes.update(list_of_game_objects)
    #     boy.body.move(list_of_game_objects, np.array([-1, 0]))
    #     boy.brain.eyes.update(list_of_game_objects)
    #     boy.brain.interpreter.update()
    #     print boy.brain.interpreter.state['got_item']
    #     #assert boy.brain.interpreter.state['got_item'] == item.delete
    #     if item.delete:
    #         list_of_game_objects = [boy, other_boy]