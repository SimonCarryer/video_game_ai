from util.helpers import *
import numpy as np


class State(object):
    def __init__(self, name, body, eyes, sticky=True):
        self.eyes = eyes
        self.body = body
        self.name = name
        self.fulfilled = False
        self.sticky = sticky

    def status(self):
        if self.sticky:
            if self.is_fulfilled():
                self.fulfilled = True
                return True
            else:
                return self.fulfilled
        else:
            return self.is_fulfilled()

    def is_fulfilled(self):
        return self.fulfilled


class LocationState(State):
    def __init__(self, name, body, eyes, rect, sticky=True):
        super(LocationState, self).__init__(name, body, eyes, sticky)
        self.rect = rect

    def is_fulfilled(self):
        return point_inside_rectangle(self.rect, self.body.coords)


class SeeObjectState(State):
    def __init__(self, name, body, eyes, object_description, sticky=False):
        super(SeeObjectState, self).__init__(name, body, eyes, sticky)
        self.object_description = object_description

    def is_fulfilled(self):
        seen = self.eyes.look_for_object(self.body.coords, self.object_description)
        if seen is not None:
            return True
        else:
            return False


class CloseToObjectState(State):
    def __init__(self, name, body, eyes, distance, object_description, sticky=False):
        super(CloseToObjectState, self).__init__(name, body, eyes, sticky)
        self.distance = distance
        self.object_description = object_description

    def is_fulfilled(self):
        seen = self.eyes.look_for_object(self.body.coords, self.object_description)
        if seen is not None:
            distance = distance_between_points(seen.coords(), self.body.coords)
            return distance <= self.distance
        else:
            return False


class ObjectInLocationState(State):
    def __init__(self, name, body, eyes, rect, object_description, sticky=True):
        super(ObjectInLocationState, self).__init__(name, body, eyes, sticky)
        self.object_description = object_description
        self.rect = rect

    def is_fulfilled(self):
        seen = self.eyes.look_for_object(self.body.coords, self.object_description)
        if seen is not None:
            return point_inside_rectangle(self.rect, seen.coords())
        else:
            return False


class AtPointState(State):
    def __init__(self, name, body, eyes, point, sticky=True):
        super(AtPointState, self).__init__(name, body, eyes, sticky)
        self.point = np.array(point)

    def is_fulfilled(self):
        distance = distance_between_points(self.point, self.body.coords)
        return distance <= 1


class SetByActionState(State):
    def __init__(self, name, body, eyes, sticky=True):
        super(SetByActionState, self).__init__(name, body, eyes, sticky)
        self.fulfilled = False

    def is_fulfilled(self):
        return self.fulfilled