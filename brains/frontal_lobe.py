from pathfinding.grid import BackgroundGrid


class FrontalLobe:
    def __init__(self, arena_width, arena_height, grid_spacing):
        self.grid = BackgroundGrid(arena_width, arena_height, grid_spacing)

    def populate_grid(self, list_of_game_objects):
        walls = [game_object for game_object in list_of_game_objects if game_object.image['kind'] == 'wall']
        self.grid.calculate_edges(walls)
        