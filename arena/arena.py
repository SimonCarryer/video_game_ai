from pygame.sprite import Group


class Arena:
    def __init__(self, SCREENRECT):
        self.w = SCREENRECT.width
        self.h = SCREENRECT.height
        self.screen_objects = []

    def add_screen_objects(self, screen_objects):
        for screen_object in screen_objects:
            self.screen_objects.append(screen_object)

    def update_screen_objects(self, screen):
        for screen_object in self.screen_objects:
            screen_object.update(screen)
