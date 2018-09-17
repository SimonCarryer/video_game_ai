from drawing.visible import Visible
from physics.moving_circle import MovingCircle
from physics.physical_object import ObstructingCircle


class Body:
    def __init__(self, coords, initial_velocity, recipe):
        self.sprite = Visible(coords,
                              recipe['radius'],
                              colour=recipe['colour'])
        self.movement = MovingCircle(coords,
                                     max_accelleration=recipe['accelleration'],
                                     initial_velocity=initial_velocity)
        self.substance = ObstructingCircle(coords,
                                           recipe['radius'],
                                           image=recipe)
        self.coords = self.movement.coords
        self.radius = recipe['radius']
        self.velocity = self.movement.velocity

    def update(self, screen):
        self.sprite.draw(self.movement.coords, screen)

    def move(self, list_of_game_objects, goal_vector):
        self.movement.set_accelleration(goal_vector)
        self.movement.move(list_of_game_objects)
        self.substance.center = self.movement.coords
        self.coords = self.movement.coords
        self.velocity = self.movement.velocity
