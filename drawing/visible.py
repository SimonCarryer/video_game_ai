import pygame


class Visible(pygame.sprite.Sprite):
    def __init__(self, coords, radius, colour=(220, 0, 0)):
        super(Visible, self).__init__()
        self.colour = colour
        self.rect = pygame.Rect(*((0, 0) + (2 * radius, 2 * radius)))
        self.change_rect_center(coords)

    def change_rect_center(self, coords):
        self.rect.centerx = int(round(coords[0]))
        self.rect.centery = int(round(coords[1]))

    def draw(self, coords, screen):
        self.change_rect_center(coords)
        pygame.draw.ellipse(screen, self.colour, self.rect)


class VisibleLine(pygame.sprite.Sprite):
    def __init__(self, start_position, end_position, colour=(0, 220, 0)):
        super(VisibleLine, self).__init__()
        self.colour = colour
        self.start_position = start_position
        self.end_position = end_position

    def draw(self, screen):
        pygame.draw.line(screen, 
                         self.colour, 
                         self.start_position, 
                         self.end_position,
                         2)


class VisibleRect(pygame.sprite.Sprite):
    def __init__(self, rect, colour=(0, 220, 0)):
        super(VisibleRect, self).__init__()
        self.rect = pygame.Rect(*rect)
        self.colour = colour

    def draw(self, screen):
        pygame.draw.rect(screen, 
                         self.colour,
                         self.rect)
