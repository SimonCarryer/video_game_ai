from drawing.visible import VisibleWall


class Wall:
    def __init__(self, start, end):
        self.sprite = VisibleWall(start, end)
        self.start = start
        self.end = end

    def update(self, screen):
        self.sprite.draw(screen)
