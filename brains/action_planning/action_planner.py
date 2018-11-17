from .plan_interpreter import PlanInterpreter
from .actions import *


class ActionGetter:
    def __init__(self, image, eyes, body):
        behaviour_dict = image['behaviour']
        self.action = Action()
        if behaviour_dict.get('target') == 'mouse pointer':
            self.action = SeekMouseAction()
        elif behaviour_dict.get('target behaviour') == 'seek':
            self.action = SeekAction(behaviour_dict.get('target'))
        elif behaviour_dict.get('target behaviour') == 'flee':
            self.action = FleeAction(behaviour_dict.get('target'))

    def update(self):
        pass


class ActionPlanner(ActionGetter):
    def __init__(self, image, eyes, body):
        self.action = Action()
        file_path = image['behaviour']['plan_file']
        start = image['behaviour']['start']
        priorities = image['behaviour']['priorities']
        self.interpreter = PlanInterpreter(body, eyes, file_path, start, priorities)
        self.interpreter.formulate_plan()

    def update(self):
        self.interpreter.update()
        self.action = self.interpreter.current_action()
        