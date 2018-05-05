from drawing.visible import Visible
from physics.moving_circle import MovingCircle
from physics.physical_object import ObstructingCircle
from brains.brain import Brain
from screen_objects.boy_recipes import boy_cookbook


class Boy():
    def __init__(self, coords, initial_velocity, boy_type):
        recipe = boy_cookbook.get_recipe(boy_type)
        self.sprite = Visible(coords,
                              recipe['radius'],
                              colour=recipe['colour'])
        self.movement = MovingCircle(coords,
                                     max_accelleration=recipe['accelleration'],
                                     initial_velocity=initial_velocity)
        recipe['name'] = self.movement.name
        self.substance = ObstructingCircle(coords,
                                           recipe['radius'],
                                           image=recipe)
        self.image = recipe
        self.brain = Brain(recipe)

    def collide(self, screen_object):
        if self.movement.name == screen_object.name:
            return None
        else:
            return self.substance.collide(screen_object)

    def coords(self):
        return self.substance.center

    def move(self, list_of_game_objects):
        goal_vector = self.brain.get_goal_vector(self.movement.coords, 
                                                 self.movement.velocity,
                                                 list_of_game_objects)
        self.movement.set_accelleration(goal_vector)
        self.movement.move(list_of_game_objects)
        self.substance.center = self.movement.coords

    def update(self, screen, list_of_game_objects):
        self.move(list_of_game_objects)
        self.sprite.draw(self.movement.coords, screen)
