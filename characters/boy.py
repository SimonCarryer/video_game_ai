from drawing.visible import Visible
from physics.moving_circle import MovingCircle
from physics.physical_object import ObstructingCircle
from brains.brain import Brain
from characters.boy_recipes import boy_recipes


class SelfImage:
    def __init__(self,
                 boy_type):
        recipe = boy_recipes[boy_type]
        self.type = boy_type
        for key in recipe:
            setattr(self, key, recipe[key])


class Boy():
    def __init__(self, coords, initial_velocity, boy_type):
        image = SelfImage(boy_type)
        self.sprite = Visible(coords,
                              image.radius,
                              colour=image.colour)
        self.movement = MovingCircle(coords,
                                     max_accelleration=image.accelleration,
                                     initial_velocity=initial_velocity)
        self.substance = ObstructingCircle(coords,
                                           image.radius)
        image.name = self.movement.name
        self.brain = Brain(image)

    def collide(self, screen_object):
        if self.movement.name == screen_object.name:
            return None
        else:
            return self.substance.collide(screen_object)

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
