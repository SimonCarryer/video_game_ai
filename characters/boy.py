from drawing.visible import Visible
from physics.moving_circle import MovingCircle
from physics.physical_object import ObstructingCircle
from brains.brain import Brain


class Boy():
    def __init__(self, coords, radius, initial_velocity):
        self.sprite = Visible(coords, radius, colour=(220, 0, 0))
        self.movement = MovingCircle(coords, initial_velocity=initial_velocity)
        self.substance = ObstructingCircle(coords, radius)
        self.brain = Brain(radius, self.movement.name)

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
