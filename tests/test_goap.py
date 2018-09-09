from brains.action_planning.plan_builder import *
from brains.action_planning.plan_interpreter import PlanInterpreter


def test_loading_plan_manifest():
    file_path = 'tests/mocks/mock_plan.json'
    manifest = manifest_from_file(file_path)
    assert manifest['states'] == ["has_item", "at_counter", "paid_for_item", "at_exit", "at_item"]


def test_creating_planner_object():
    file_path = 'tests/mocks/mock_plan.json'
    manifest = manifest_from_file(file_path)
    plan = create_plan(manifest)
    assert plan.values == {u'at_counter': -1, u'paid_for_item': -1, u'has_item': -1, u'at_exit': -1, u'at_item': -1}


def test_initialise_interpreter():
    file_path = 'tests/mocks/mock_plan.json'
    start = {'has_item': False, 'at_counter': False, 'paid_for_item': False, 'at_exit': False, 'at_item': False}
    goal = {'has_item': True, 'paid_for_item': True, 'at_exit': True}
    interpreter = PlanInterpreter(file_path, start, goal)
    desired = [u'go_to_item', u'get_item', u'go_to_counter', u'pay_for_item', u'go_to_exit']
    assert [node['name'] for node in interpreter.path] == desired


def test_calculate_state():
    file_path = 'tests/mocks/mock_plan.json'
    start = {'has_item': False, 'at_counter': False, 'paid_for_item': False, 'at_exit': False, 'at_item': False}
    goal = {'has_item': True, 'paid_for_item': True, 'at_exit': True}
    interpreter = PlanInterpreter(file_path, start, goal)
    assert interpreter.calculate_state() == 'go_to'
    interpreter.path = interpreter.path[1:]
    assert interpreter.calculate_state() == 'perform_action'
    interpreter.path = []
    assert interpreter.calculate_state() == 'idle'


def test_build_action_dict():
    file_path = 'tests/mocks/mock_plan_patrol.json'
    manifest = manifest_from_file(file_path)
    action_dict = parse_actions(manifest)
    assert action_dict.keys() == [u'go_to_point_1', u'go_to_point_3', u'go_to_point_2', u'go_to_point_4']


def test_get_action():
    file_path = 'tests/mocks/mock_plan_patrol.json'
    start = {"at_point_1": True, "at_point_2": False, "at_point_3": False, "at_point_4": False, "visited_point_1": True}
    goal = {"at_point_4": True}
    interpreter = PlanInterpreter(file_path, start, goal)
    action = interpreter.current_action()
    assert action.goal() == [10, 500]