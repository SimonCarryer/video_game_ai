from drawing.visible import Visible
from physics.moving_circle import MovingCircle
from brains.brain import Brain


class Boy():
    def __init__(self, coords, initial_velocity):
        self.sprite = Visible(coords, (15, 15), colour=(220, 0, 0))
        self.movement = MovingCircle(coords, initial_velocity=initial_velocity)
        self.brain = Brain()

    def collide(self, screen_object):
        return None

    def update(self, screen, list_of_walls):
        goal_vector = self.brain.get_goal_vector(self.movement.coords, 
                                                 self.movement.velocity)
        self.movement.set_accelleration(goal_vector)
        self.movement.move(list_of_walls)
        self.sprite.draw(self.movement.coords, screen)
