from brains.action_planning.states import *
from brains.eyes import Eyes
from screen_objects.boy import Boy
from mocks.mock_body_parts import *
import numpy as np


def test_base_state_class():
    eyes = MockEyes()
    body = MockBody()
    state = State('test_state', body, eyes)
    assert not state.is_fulfilled()


def test_location_state():
    eyes = MockEyes()
    body = MockBody()
    rect = np.array([[0, 0], [100, 100]])
    state = LocationState('test_state', body, eyes, rect)
    assert state.is_fulfilled()
    rect = np.array([[100, 100], [200, 200]])
    state = LocationState('test_state', body, eyes, rect)
    assert not state.is_fulfilled()


def test_object_visible_state():
    eyes = Eyes()
    body = MockBody()
    boy = Boy(np.array((2.0, 2.0)), np.array((0.0, 0.0)), 'tootling boy')
    state = SeeObjectState('test_state', body, eyes, 100, {'colour': (0, 0, 220)})
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
    state = ObjectInLocationState('test_state', body, eyes, rect, 100, {'colour': (0, 0, 220)})
    assert not state.is_fulfilled()
    eyes.update([boy])
    assert state.is_fulfilled()
    other_boy = Boy(np.array((12.0, 2.0)), np.array((0.0, 0.0)), 'tootling boy')
    eyes.update([other_boy])
    assert not state.is_fulfilled()