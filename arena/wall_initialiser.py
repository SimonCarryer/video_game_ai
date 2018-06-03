from screen_objects.wall import Wall, Boundary
from random import shuffle, randrange
import numpy as np


def make_maze_nodes(w=8, h=8):
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

vertical_walls, horizontal_walls = make_maze_nodes()


def wall_from_nodes(nodes):
    return Wall(nodes[0], nodes[1])

walls = []

grid_spacing=640/8

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




# walls = []

# shape_1 = [(200, 200),
#            (300, 200),
#            (300, 300),
#            (400, 300),
#            (400, 400)
#            ]

# shape_2 = [(x - 100, y + 100) for x, y in shape_1]

# shapes = [shape_1, shape_2]

# for shape in shapes:
#     for i in range(len(shape)-1):
#         walls.append(Wall(shape[i], shape[i+1]))


bounds = [Boundary((0, 0), (640, 0)),
          Boundary((640, 0), (640, 640)),
          Boundary((640, 640), (0, 640)),
          Boundary((0, 640), (0, 0))
          ]
