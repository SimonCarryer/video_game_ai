from util.helpers import *
import numpy as np


class State(object):
    def __init__(self, name, body, eyes, requirements=None, state=None, sticky=True):
        self.global_state = state
        self.requirements = requirements
        if self.requirements is None:
            self.requirements = {}
        if self.global_state is None:
            self.global_state = {}
        self.eyes = eyes
        self.body = body
        self.name = name
        self.fulfilled = False
        self.sticky = sticky

    def requirements_met(self):
        return self.requirements.viewitems() <= self.global_state.viewitems()

    def status(self):
        if self.sticky:
            if self.is_fulfilled() and self.requirements_met():
                self.fulfilled = True
                return True
            else:
                return self.fulfilled
        else:
            return self.is_fulfilled() and self.requirements_met()

    def is_fulfilled(self):
        return self.fulfilled


class LocationState(State):
    def __init__(self, name, body, eyes, rect, requirements=None, state=None, sticky=True):
        super(LocationState, self).__init__(name, body, eyes, requirements, state, sticky)
        self.rect = rect

    def is_fulfilled(self):
        return point_inside_rectangle(self.rect, self.body.coords)


class SeeObjectState(State):
    def __init__(self, name, body, eyes, object_description, requirements=None, state=None, sticky=False):
        super(SeeObjectState, self).__init__(name, body, eyes, requirements, state, sticky)
        self.object_description = object_description

    def is_fulfilled(self):
        seen = self.eyes.look_for_object(self.body.coords, self.object_description)
        if seen is not None:
            return True
        else:
            return False


class CloseToObjectState(State):
    def __init__(self, name, body, eyes, distance, object_description, requirements=None, state=None, sticky=False):
        super(CloseToObjectState, self).__init__(name, body, eyes, requirements, state, sticky)
        self.distance = distance
        self.object_description = object_description

    def is_fulfilled(self):
        seen = self.eyes.look_for_object(self.body.coords, self.object_description)
        if seen is not None:
            distance = distance_between_points(seen.coords(), self.body.coords)
            return distance <= self.distance
        else:
            return False


class PickedUpItemState(State):
    def __init__(self, name, body, eyes, object_description, requirements=None, state=None, sticky=False):
        super(PickedUpItemState, self).__init__(name, body, eyes, requirements, state, sticky)
        self.object_description = object_description

    def is_fulfilled(self):
        seen_item = self.eyes.look_for_object(self.body.coords, self.object_description)
        if seen_item is not None:
            pick_up_distance = self.body.radius + seen_item.radius
            distance = distance_between_points(seen_item.coords(), self.body.coords)
            if distance <= pick_up_distance and self.requirements_met():
                seen_item.delete = True
                return True
        else:
            return False

class ObjectInLocationState(State):
    def __init__(self, name, body, eyes, rect, object_description, requirements=None, state=None, sticky=True):
        super(ObjectInLocationState, self).__init__(name, body, eyes, requirements, state, sticky)
        self.object_description = object_description
        self.rect = rect

    def is_fulfilled(self):
        seen = self.eyes.look_for_object(self.body.coords, self.object_description)
        if seen is not None:
            return point_inside_rectangle(self.rect, seen.coords())
        else:
            return False


class AtPointState(State):
    def __init__(self, name, body, eyes, point, requirements=None, state=None, sticky=True):
        super(AtPointState, self).__init__(name, body, eyes, requirements, state, sticky)
        self.point = np.array(point)

    def is_fulfilled(self):
        distance = distance_between_points(self.point, self.body.coords)
        return distance <= 10


class SetByActionState(State):
    def __init__(self, name, body, eyes, requirements=None, state=None, sticky=True):
        super(SetByActionState, self).__init__(name, body, eyes, requirements, state, sticky)
        self.fulfilled = False

    def is_fulfilled(self):
        return self.fulfilled


class RightRoleState(State):
    def __init__(self, name, body, eyes, role, requirements=None, state=None, sticky=True):
        super(RightRoleState, self).__init__(name, body, eyes, requirements, state, sticky)
        self.role = role
        self.fulfilled = False

    def is_fulfilled(self):
        return self.body.recipe.get('role') == self.role