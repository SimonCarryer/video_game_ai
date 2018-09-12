from .goap import Planner, Action_List
from .actions import *
from .states import *
import json


def manifest_from_file(plan_file_path):
    with open(plan_file_path, 'r') as f:
        plan_manifest = json.loads(f.read())
    return plan_manifest


def create_plan(plan_manifest):
    states = [state['name'] for state in plan_manifest['states']]
    plan = Planner(*states)
    actions = Action_List()
    for action in plan_manifest['actions']:
        actions.add_condition(action['name'], **action['conditions'])
        actions.add_reaction(action['name'], **action['reactions'])
    plan.set_action_list(actions)
    return plan


def parse_actions(plan_manifest):
    action_dict = {}
    for action in plan_manifest['actions']:
        if action['type'] == 'go_to':
            action_object = GoToAction(action['goal'])
        action_dict[action['name']] = action_object
    return action_dict

state_dict = {
    "at_point": AtPointState,
    "set_by_action": SetByActionState,
    "in_location": LocationState,
    "close_to_object": SeeObjectState
}


def parse_states(plan_manifest, body, eyes):
    parsed_states = []
    for state in plan_manifest['states']:
        state_type = state.pop('type')
        state['eyes'] = eyes
        state['body'] = body
        obj = state_dict[state_type](**state)
        parsed_states.append(obj)
    return parsed_states
