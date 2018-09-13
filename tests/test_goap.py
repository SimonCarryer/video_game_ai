from brains.action_planning.plan_builder import *
from brains.action_planning.plan_interpreter import PlanInterpreter
from mocks.mock_body_parts import *
from brains.action_planning.actions import *


def test_loading_plan_manifest():
    file_path = 'tests/mocks/mock_plan.json'
    manifest = manifest_from_file(file_path)
    states = [state['name'] for state in manifest['states']]
    assert states == ["has_item", "at_counter", "paid_for_item", "at_exit", "at_item"]


def test_creating_planner_object():
    file_path = 'tests/mocks/mock_plan.json'
    manifest = manifest_from_file(file_path)
    plan = create_plan(manifest)
    assert plan.values == {u'at_counter': -1, u'paid_for_item': -1, u'has_item': -1, u'at_exit': -1, u'at_item': -1}


def test_initialise_interpreter():
    file_path = 'tests/mocks/mock_plan.json'
    start = {'has_item': False, 'at_counter': False, 'paid_for_item': False, 'at_exit': False, 'at_item': False}
    goal = {'has_item': True, 'paid_for_item': True, 'at_exit': True}
    body = MockBody()
    eyes = MockEyes()
    interpreter = PlanInterpreter(body, eyes, file_path, start, goal)
    desired = [u'go_to_item', u'get_item', u'go_to_counter', u'pay_for_item', u'go_to_exit']
    assert [node['name'] for node in interpreter.path] == desired


def test_build_action_dict():
    file_path = 'tests/mocks/mock_plan_patrol.json'
    manifest = manifest_from_file(file_path)
    action_dict = parse_actions(manifest)
    assert action_dict.keys() == [u'go_to_point_1', u'go_to_point_3', u'go_to_point_2', u'go_to_point_4']


def test_get_action():
    file_path = 'tests/mocks/mock_plan_patrol.json'
    start = {"at_point_1": True, "at_point_2": False, "at_point_3": False, "at_point_4": False}
    goal = {"at_point_1": True, "at_point_2": True, "at_point_3": True, "at_point_4": True}
    body = MockBody()
    eyes = MockEyes()
    interpreter = PlanInterpreter(body, eyes, file_path, start, goal)
    action = interpreter.current_action()
    assert (action.goal() == [10, 500]).all()


def test_parse_states():
    body = MockBody()
    eyes = MockEyes()
    manifest = {'states':
                [{"name": "test_state_1",
                  "type": "at_point",
                  "point": [0, 0]}]}
    state = parse_states(manifest, body, eyes)[0]
    assert (state.point == [0, 0]).all()


def test_update_state():
    file_path = 'tests/mocks/mock_plan_patrol.json'
    start = {"at_point_1": False, "at_point_2": False, "at_point_3": False, "at_point_4": False}
    goal = {"at_point_1": True, "at_point_2": True, "at_point_3": True, "at_point_4": True}
    body = MockBody()
    eyes = MockEyes()
    interpreter = PlanInterpreter(body, eyes, file_path, start, goal)
    action = interpreter.current_action()
    assert (action.goal() == [10, 10]).all()
    body.coords = [10, 10]
    interpreter.update_state()
    interpreter.formulate_plan()
    action = interpreter.current_action()
    assert (action.goal() == [10, 500]).all()


def test_action_succeed():
    conditions = {'test_condition': True}
    action = Action(conditions=conditions)
    state = {'test_condition': True}
    assert action.succeed(state)
    state = {'test_condition': True, 'other_condition': False}
    assert action.succeed(state)
    conditions = {'test_condition': True, 'other_condition': True}
    action = Action(conditions=conditions)
    state = {'test_condition': True}
    assert not action.succeed(state)
    state = {'test_condition': False}
    assert not action.succeed(state)
