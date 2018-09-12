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


class SeeObjectState(State):
    def __init__(self, name, body, eyes, distance, object_description):
        super(SeeObjectState, self).__init__(name, body, eyes)
        self.distance = distance
        self.object_description = object_description

    def is_fulfilled(self):
        seen = self.eyes.look_for_object(self.body.coords, self.distance, self.object_description)
        if seen is not None:
            return True
        else:
            return False


class ObjectInLocationState(State):
    def __init__(self, name, body, eyes, rect, distance, object_description):
        super(ObjectInLocationState, self).__init__(name, body, eyes)
        self.distance = distance
        self.object_description = object_description
        self.rect = rect

    def is_fulfilled(self):
        seen = self.eyes.look_for_object(self.body.coords, self.distance, self.object_description)
        if seen is not None:
            return point_inside_rectangle(self.rect, seen.coords())
        else:
            return False


class AtPointState(State):
    def __init__(self, name, body, eyes, point):
        super(AtPointState, self).__init__(name, body, eyes)
        self.point = point

    def is_fulfilled(self):
        distance = distance_between_points(self.point, self.body.coords)
        return distance <= 20


class SetByActionState(State):
    def __init__(self, name, body, eyes):
        super(SetByActionState, self).__init__(name, body, eyes)
        self.fulfilled = False

    def is_fulfilled(self):
        return self.fulfilled