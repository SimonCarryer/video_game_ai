from screen_objects.screen_object import ScreenObject
from bodies.body import Body
from brains.brain import Brain
from brains.pathfinding_brain import PathFindingBrain
from screen_objects.boy_recipes import boy_cookbook


class Boy(ScreenObject):
    def __init__(self, coords, initial_velocity, boy_type):
        super(Boy, self).__init__()
        recipe = boy_cookbook.get_recipe(boy_type)
        self.body = Body(coords, initial_velocity, recipe)
        self.image = recipe 
        self.brain = Brain(self.body, recipe)

    def collide(self, colliding_object):
        return self.body.substance.collide(colliding_object)

    def coords(self):
        return self.body.coords

    def move(self, list_of_game_objects):
        goal_vector = self.brain.get_goal_vector(list_of_game_objects)
        self.body.move(list_of_game_objects, goal_vector)

    def update(self, screen, list_of_game_objects):
        list_of_game_objects = [game_object for game_object in list_of_game_objects if game_object.name != self.name]
        self.brain.update(list_of_game_objects)
        self.move(list_of_game_objects)
        self.body.update(screen)