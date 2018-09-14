import uuid


class ScreenObject(object):
    def __init__(self):
        self.name = uuid.uuid4().bytes
        self.delete = False
        self.image = {}
