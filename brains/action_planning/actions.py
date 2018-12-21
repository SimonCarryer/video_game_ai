import numpy as np


class Action(object):
    def __init__(self, reactions={}, conditions={}):
        self.reactions = reactions,
        self.conditions = conditions

    def succeed(self, state):
        return self.reactions[0].viewitems() <= state.viewitems()

    def behaviour(self):
        return 'seek'

    def target(self):
        return None

    def goal(self):
        return None


class PerformAction(Action):
    def __init__(self, delay, reactions=None, conditions=None):
        super(PerformAction, self).__init__(reactions, conditions)
        self.delay = delay
        self.counter = 0

    def succeed(self, state):
        success = False
        if self.conditions.viewitems() <= state.viewitems():
            self.counter += 1
            if self.counter >= self.delay:
                self.counter = 0
                success = True
        return success

    def behaviour(self):
        return 'stop'


class GoToAction(Action):
    def __init__(self, goal, reactions=None, conditions=None):
        super(GoToAction, self).__init__(reactions, conditions)
        self.goal_location = np.array(goal)

    def behaviour(self):
        return 'seek'

    def goal(self):
        return self.goal_location


class SeekAction(Action):
    def __init__(self, object_description, reactions=None, conditions=None):
        super(SeekAction, self).__init__(reactions, conditions)
        self.object_description = object_description

    def behaviour(self):
        return 'seek'

    def target(self):
        return self.object_description


class SeekMouseAction(Action):
    def __init__(self, reactions=None, conditions=None):
        super(SeekMouseAction, self).__init__(reactions, conditions)

    def behaviour(self):
        return 'seek'

    def target(self):
        return 'mouse pointer'


class FleeAction(Action):
    def __init__(self, object_description, reactions=None, conditions=None):
        super(FleeAction, self).__init__(reactions, conditions)
        self.object_description = object_description

    def behaviour(self):
        return 'flee'

    def target(self):
        return self.object_description
