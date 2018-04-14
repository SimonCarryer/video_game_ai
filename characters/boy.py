from drawing.visible import Visible
from physics.moving_circle import MovingCircle
from brains.brain import Brain


class Boy():
    def __init__(self, coords, radius, initial_velocity):
        self.sprite = Visible(coords, radius, colour=(220, 0, 0))
        self.movement = MovingCircle(coords, initial_velocity=initial_velocity)
        self.brain = Brain(radius)

    def collide(self, screen_object):
        return None

    def update(self, screen, list_of_game_objects):
        goal_vector = self.brain.get_goal_vector(self.movement.coords, 
                                                 self.movement.velocity,
                                                 list_of_game_objects)
        self.movement.set_accelleration(goal_vector)
        self.movement.move(list_of_game_objects)
        self.sprite.draw(self.movement.coords, screen)
