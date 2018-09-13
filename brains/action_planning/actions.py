import numpy as np


class Action(object):
    def __init__(self, reactions=None, conditions=None):
        self.reactions = reactions,
        self.conditions = conditions

    def succeed(self, state):
        return state.viewitems() <= self.conditions.viewitems()

    def behaviour(self):
        return 'seek'

    def target(self):
        return None

    def goal(self):
        return None


class GoToAction(Action):
    def __init__(self, goal, reactions=None, conditions=None):
        super(GoToAction, self).__init__(reactions, conditions)
        self.goal_location = np.array(goal)

    def behaviour(self):
        return 'seek'

    def goal(self):
        return self.goal_location


class SeekAction(Action):
    def __init__(self, target_description, reactions=None, conditions=None):
        super(SeekAction, self).__init__(reactions, conditions)
        self.target_description = target_description

    def behaviour(self):
        return 'seek'

    def target(self):
        return self.target_description


class FleeAction(Action):
    def __init__(self, target_description, reactions=None, conditions=None):
        super(FleeAction, self).__init__(reactions, conditions)
        self.target_description = target_description

    def behaviour(self):
        return 'flee'

    def target(self):
        return self.target_description
