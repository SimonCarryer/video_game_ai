from drawing.visible import Visible
from physics.moving_object import Moving


class Boy():
    def __init__(self, coords, initial_velocity):
        self.sprite = Visible(coords, (15, 15), colour=(220, 0, 0))
        self.movement = Moving(coords, initial_velocity=initial_velocity)

    def update(self, screen):
        self.movement.move()
        self.sprite.draw(self.movement.coords, screen)
