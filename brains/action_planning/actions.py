import numpy as np


class Action:
    def __init__(self):
        pass

    def target(self):
        return None

    def goal(self):
        return None

    def succeed(self, current_location):
        return False


class GoToAction(Action):
    def __init__(self, goal_location):
        self.goal_location = goal_location

    def goal(self):
        return self.goal_location
