import pygame


class Visible:
    __init__(self, x_pos, y_pos, x_size, y_size, colour=(220, 0, 0)):
        self.colour = colour
        self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
