from arena.arena import Arena
from pygame.locals import *
from arena.wall_initialiser import initialise_walls
from arena.boy_initialiser import initialise_boys
from brains.pathfinding.grid import BackgroundGrid
import pygame

SCREENRECT = Rect(0, 0, 640, 640)

pygame.init()
winstyle = 0
bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
screen = pygame.display.set_mode((640, 640), winstyle, bestdepth)

arena = Arena(SCREENRECT)

method = 'pathfinding'

initialise_walls(arena, method)
initialise_boys(arena, method)

clock = pygame.time.Clock()


def main(screen, arena):
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        screen.fill((30, 30, 30))
        arena.update_screen_objects(screen)
        pygame.display.flip()
        clock.tick_busy_loop(30)


if __name__ == '__main__':
    main(screen, arena)
