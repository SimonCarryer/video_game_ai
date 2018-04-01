from drawing.visible import VisibleWall
from physics.physical_object import PhysicalWall


class Wall:
    def __init__(self, start, end):
        self.sprite = VisibleWall(start, end)
        self.substance = PhysicalWall(start, end)
        self.start = start
        self.end = end

    def update(self, screen, list_of_walls):
        self.sprite.draw(screen)

    def collide(self, movement_start, movement_end):
        return self.substance.collide(movement_start, movement_end)
