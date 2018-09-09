from util.helpers import *


class State(object):
    def __init__(self, name, body, eyes):
        self.eyes = eyes
        self.body = body
        self.name = name

    def is_fulfilled(self):
        return False


class LocationState(State):
    def __init__(self, name, body, eyes, rect):
        super(LocationState, self).__init__(name, body, eyes)
        self.rect = rect

    def is_fulfilled(self):
        return point_inside_rectangle(self.rect, self.body.coords)
