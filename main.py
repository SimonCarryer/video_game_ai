from arena.arena import Arena
from screen_objects.boy import Boy
from pygame.locals import *
from arena.wall_initialiser import walls, bounds
from brains.pathfinding.grid import BackgroundGrid
import pygame

SCREENRECT = Rect(0, 0, 640, 640)

pygame.init()
winstyle = 0
bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
screen = pygame.display.set_mode((640, 640), winstyle, bestdepth)

arena = Arena(SCREENRECT)
boy = Boy((100, 105), (20, 0), 'tootling boy')
scaredy_boy = Boy((200, 100), (-20, 0), 'scaredy boy')

hungry_boy = Boy((200, 400), (20, 0), 'hungry boy')
friendly_boy = Boy((400, 400), (20, 0), 'friendly boy')

arena.add_screen_objects([hungry_boy, friendly_boy, scaredy_boy, boy])
arena.add_screen_objects(walls)
arena.add_screen_objects(bounds)

grid = BackgroundGrid(arena.w, arena.h, 57)
grid.calculate_edges(walls)

clock = pygame.time.Clock()


def main(screen, arena):
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        screen.fill((30, 30, 30))
        grid.draw(screen)
        arena.update_screen_objects(screen)
        pygame.display.flip()
        clock.tick_busy_loop(30)


if __name__ == '__main__':
    main(screen, arena)
