from pygame.sprite import Group


class Arena:
    def __init__(self, SCREENRECT):
        self.w = SCREENRECT.width
        self.h = SCREENRECT.height
        self.screen_objects = []
        self.managers = []

    def add_screen_objects(self, screen_objects):
        for screen_object in screen_objects:
            self.screen_objects.append(screen_object)

    def delete_screen_objects(self):
        self.screen_objects = [obj for obj in self.screen_objects if not obj.delete]

    def update_screen_objects(self, screen):
        for screen_object in self.screen_objects:
            screen_object.update(screen, self.screen_objects)
        self.delete_screen_objects()

    def update_managers(self):
        for manager in self.managers:
            manager.update(self.screen_objects)
