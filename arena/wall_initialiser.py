from screen_objects.wall import Wall, Boundary

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


bounds = [Boundary((0, 0), (640, 0)),
          Boundary((640, 0), (640, 640)),
          Boundary((640, 640), (0, 640)),
          Boundary((0, 640), (0, 0))
          ]
