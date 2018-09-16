from .goap import Planner, Action_List
from plan_builder import *
from .actions import Action


class PlanInterpreter():
    def __init__(self,
                 body,
                 eyes,
                 plan_file_path,
                 start_state,
                 priorities):
        self.manifest = manifest_from_file(plan_file_path)
        self.planner = create_plan(self.manifest)
        self.action_dict = parse_actions(self.manifest)
        self.states = parse_states(self.manifest, body, eyes)
        self.state = start_state
        self.priorities = priorities
        self.goal = self.manifest['goals'][priorities[0]]
        self.path = self.formulate_plan()

    def determine_goal(self):
        for priority in self.priorities:
            goal = self.manifest['goals'][priority]
            plan = self.formulate_plan(goal=goal)
            if len(plan) > 0:
                self.goal = goal
                break

    def formulate_plan(self, goal=None):
        if goal is None:
            goal = self.goal
        self.planner.set_start_state(**self.state)
        self.planner.set_goal_state(**goal)
        return self.planner.calculate()

    def update_state(self):
        for state in self.states:
            self.state[state.name] = state.status()
        current_action = self.current_action()
        if current_action.succeed(self.state):
            current_action.reactions
        if self.succeed():
            self.set_sticky_states_to_false()

    def update(self):
        self.update_state()
        self.determine_goal()
        self.path = self.formulate_plan()

    def set_sticky_states_to_false(self):
        completed_goals = [i for i in self.goal.keys()]
        for state in self.states:
            if state.name in completed_goals:
                print "set to false: %s" % state.name
                state.fulfilled = False

    def succeed(self):
        return self.goal.viewitems() <= self.state.viewitems()

    def current_action(self):
        if len(self.path) > 0:
            action = self.path[0]['name']
            return self.action_dict[action]
        else:
            return Action()