from util.helpers import just_walls


class Memory:
    def __init__(self):
        self.known_walls = []

    def remember_walls(self, list_of_visible_objects):
        walls = just_walls(list_of_visible_objects)
        for wall in walls:
            if wall not in self.known_walls:
                wall.sprite.colour = (0, 0, 220)
                self.known_walls.append(wall)