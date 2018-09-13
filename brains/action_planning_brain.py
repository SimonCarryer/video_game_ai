from .brain import Brain
from action_planning.plan_interpreter import PlanInterpreter


class ActionPlanningBrain(Brain):
    def __init__(self, body, image):
        super(ActionPlanningBrain, self).__init__(body, image)
        file_path = image['behaviour']['plan_file']
        start = image['behaviour']['start']
        goal = image['behaviour']['goal']
        self.interpreter = PlanInterpreter(self.body, self.eyes, file_path, start, goal)
        self.interpreter.formulate_plan()

    def update(self, list_of_game_objects):
        super(ActionPlanningBrain, self).update(list_of_game_objects)
        self.interpreter.update_state()
        self.interpreter.formulate_plan()
        self.action = self.interpreter.current_action()