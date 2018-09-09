from .goap import Planner, Action_List
from .actions import *
import json


def manifest_from_file(plan_file_path):
    with open(plan_file_path, 'r') as f:
        plan_manifest = json.loads(f.read())
    return plan_manifest


def create_plan(plan_manifest):
    plan = Planner(*plan_manifest['states'])
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
