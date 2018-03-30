import pygame


class Visible(pygame.sprite.Sprite):
    def __init__(self, coords, size, colour=(220, 0, 0)):
        super(Visible, self).__init__()
        self.colour = colour
        self.rect = pygame.Rect(*((0, 0) + size))
        self.change_rect_center(coords)

    def change_rect_center(self, coords):
        self.rect.centerx = int(round(coords[0]))
        self.rect.centery = int(round(coords[1]))

    def draw(self, coords, screen):
        self.change_rect_center(coords)
        pygame.draw.ellipse(screen, self.colour, self.rect)
