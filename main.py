from arena.arena import Arena
from characters.boy import Boy
from objects.wall import Wall
from pygame.locals import *
import pygame

SCREENRECT = Rect(0, 0, 640, 640)

pygame.init()
winstyle = 0
bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
screen = pygame.display.set_mode((640, 640), winstyle, bestdepth)

arena = Arena(SCREENRECT)
boy = Boy((100, 100), (20, 0))
wall = Wall((200, 200), (300, 200))

arena.add_screen_objects([boy, wall])


def main(screen, arena):
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        screen.fill((30, 30, 30))
        arena.update_screen_objects(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main(screen, arena)
