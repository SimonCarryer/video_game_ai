from screen_objects.wall import Wall, Boundary
from random import shuffle, randrange
from screen_objects.location import Location
import numpy as np


def make_maze_nodes(w=12, h=12):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [[((x, y), (x, y+1)) for x in range(w)] for y in range(h)] + [[]]
    hor = [[((x, y), (x+1, y)) for x in range(w)] for y in range(h + 1)]
    
    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = None
            if yy == y: ver[y][max(x, xx)] = None
            walk(xx, yy)
            
    walk(randrange(w), randrange(h))
    return [[None] + i[1:] for i in ver[:-1]], [[None] * w] + hor[1:]


def wall_from_nodes(nodes):
    return Wall(nodes[0], nodes[1])


def maze():
    vertical_walls, horizontal_walls = make_maze_nodes()
    walls = []

    grid_spacing=640/12

    for row in vertical_walls:
        for nodes in row:
            if nodes is not None:
                nodes = np.array(nodes)
                walls.append(wall_from_nodes(nodes * grid_spacing))

    for row in horizontal_walls:
        for nodes in row:
            if nodes is not None:
                nodes = np.array(nodes)
                walls.append(wall_from_nodes(nodes * grid_spacing))
    return walls


def shape():
    walls = []

    shape_1 = [(200, 200),
            (300, 200),
            (300, 300),
            (400, 300),
            (400, 400)
            ]

    shape_2 = [(x - 100, y + 100) for x, y in shape_1]

    shapes = [shape_1, shape_2]

    for shape in shapes:
        for i in range(len(shape)-1):
            walls.append(Wall(shape[i], shape[i+1]))
    return walls


def locations():
    ailse1 = Wall((100, 100), (100, 500))
    ailse2 = Wall((200, 100), (200, 500))
    ailse3 = Wall((300, 100), (300, 500))
    location = Location(((100, 100), (150, 150)))
    return [location, ailse1, ailse2, ailse3]


def initialise_walls(arena, method):
    if method == 'steering':
        walls = shape()
    elif method == 'pathfinding':
        walls = maze()
    elif method == 'goap':
        walls = locations()
    bounds = [Boundary((0, 0), (arena.h, 0)),
              Boundary((arena.h, 0), (arena.h, arena.w)),
              Boundary((arena.h, arena.w), (0, arena.w)),
              Boundary((0, arena.w), (0, 0))
              ]
    arena.add_screen_objects(walls)
    arena.add_screen_objects(bounds)
