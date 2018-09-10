from .goap import Planner, Action_List
from plan_builder import *


class PlanInterpreter():
    def __init__(self, plan_file_path, start_state, goal_state):
        manifest = manifest_from_file(plan_file_path)
        self.planner = create_plan(manifest)
        self.action_dict = parse_actions(manifest)
        self.state = start_state
        self.goal = goal_state
        self.path = self.formulate_plan()
        self.state = self.calculate_state()

    def formulate_plan(self):
        self.planner.set_start_state(**self.state)
        self.planner.set_goal_state(**self.goal)
        return self.planner.calculate()

    def calculate_state(self):
        if len(self.path) == 0:
            state = 'idle'
        else:
            current_action = self.path[0]['name']
            if current_action[:5] == 'go_to':
                state = 'go_to'
            else:
                state = 'perform_action'
        return state

    def update_state(self, state_dict):
        self.state.update(state_dict)

    def current_action(self):
        action = self.path[0]['name']
        return self.action_dict[action]

    def goal_achieved(self):
        self.path = self.path[1:]