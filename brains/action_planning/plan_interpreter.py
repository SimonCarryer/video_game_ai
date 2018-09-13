from .goap import Planner, Action_List
from plan_builder import *


class PlanInterpreter():
    def __init__(self,
                 body,
                 eyes,
                 plan_file_path,
                 start_state,
                 goal_state):
        manifest = manifest_from_file(plan_file_path)
        self.planner = create_plan(manifest)
        self.action_dict = parse_actions(manifest)
        self.states = parse_states(manifest, body, eyes)
        self.state = start_state
        self.goal = goal_state
        self.formulate_plan()

    def formulate_plan(self):
        self.planner.set_start_state(**self.state)
        self.planner.set_goal_state(**self.goal)
        self.path = self.planner.calculate()

    def update_state(self):
        for state in self.states:
            self.state[state.name] = state.status()
        current_action = self.current_action()
        if current_action.succeed(self.state):
            current_action.reactions

    def current_action(self):
        action = self.path[0]['name']
        return self.action_dict[action]
