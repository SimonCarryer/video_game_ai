from brains.action_planning.states import *
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