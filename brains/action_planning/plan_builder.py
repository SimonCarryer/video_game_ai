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

action_dict = {
    'go_to': GoToAction,
    'action': Action,
    'seek': SeekAction,
    'flee': FleeAction,
    'perform': PerformAction
}


def parse_actions(plan_manifest):
    actions = {}
    for action in plan_manifest['actions']:
        obj = action_dict[action['type']]
        stripped_action = {k: v for k, v in action.items() if k not in ['name', 'type']}
        actions[action['name']] = obj(**stripped_action)
    return actions

state_dict = {
    "at_point": AtPointState,
    "set_by_action": SetByActionState,
    "in_location": LocationState,
    "see_object": SeeObjectState,
    "close_to_object": CloseToObjectState,
    "pick_up_item": PickedUpItemState,
    "object_in_location": ObjectInLocationState,
    "set_by_action": State,
    "role": RightRoleState
}


def parse_states(plan_manifest, body, eyes, global_state=None):
    parsed_states = []
    for state in plan_manifest['states']:
        state_type = state.pop('type')
        state['eyes'] = eyes
        state['body'] = body
        state['state'] = global_state
        if state.get('location'):
            state['rect'] = plan_manifest['locations'][state.pop('location')]
        obj = state_dict[state_type](**state)
        parsed_states.append(obj)
    return parsed_states
