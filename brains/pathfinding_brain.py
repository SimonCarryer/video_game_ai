from .brain import Brain
from .memory import Memory
from .frontal_lobe import FrontalLobe


class PathFindingBrain(Brain):
    def __init__(self, body, image):
        super(PathFindingBrain, self).__init__(body, image)

    def update(self, list_of_game_objects):
        super(PathFindingBrain, self).update(list_of_game_objects)
        visible = self.eyes.visible_objects(self.body.coords)
        self.memory.remember_walls(visible)
        self.frontal_lobe.update_grid(self.memory.known_walls)

    def initialise_frontal_lobe(self, arena_height, arena_width, grid_spacing, list_of_game_objects):
        self.memory = Memory()
        self.frontal_lobe = FrontalLobe(arena_height, arena_width, grid_spacing)
        self.frontal_lobe.populate_grid(list_of_game_objects)