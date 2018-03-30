from drawing.visible import Visible
from physics.moving_object import Moving
from brains.brain import Brain


class Boy():
    def __init__(self, coords, initial_velocity):
        self.sprite = Visible(coords, (15, 15), colour=(220, 0, 0))
        self.movement = Moving(coords, initial_velocity=initial_velocity)
        self.brain = Brain()

    def update(self, screen):
        goal_vector = self.brain.get_goal_vector(self.movement.coords, 
                                                 self.movement.velocity)
        self.movement.set_accelleration(goal_vector)
        self.movement.move()
        self.sprite.draw(self.movement.coords, screen)
