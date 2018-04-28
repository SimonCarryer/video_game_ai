from arena.arena import Arena
from screen_objects.boy import Boy
from screen_objects.wall import Wall, Boundary
from pygame.locals import *
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

wall = Wall((200, 200), (300, 200))
other_wall = Wall((300, 200), (300, 300))
bound1 = Boundary((0, 0), (640, 0))
bound2 = Boundary((640, 0), (640, 640))
bound3 = Boundary((640, 640), (0, 640))
bound4 = Boundary((0, 640), (0, 0))


arena.add_screen_objects([boy, scaredy_boy, hungry_boy, friendly_boy,
                        wall, other_wall,
                        bound1, bound2, bound3, bound4])

clock = pygame.time.Clock()


def main(screen, arena):
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        screen.fill((30, 30, 30))
        arena.update_screen_objects(screen)
        pygame.display.flip()
        clock.tick_busy_loop(35)


if __name__ == '__main__':
    main(screen, arena)
