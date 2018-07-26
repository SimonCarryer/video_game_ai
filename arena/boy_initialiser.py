from screen_objects.boy import Boy


def pathfinding_boy(arena):
    hungry_boy = Boy((200, 400), (20, 0), 'pathfinding boy')
    hungry_boy.initialise_frontal_lobe(arena.h, arena.w, arena.screen_objects)
    return [hungry_boy]


def all_the_boys():
    boy = Boy((100, 105), (20, 0), 'tootling boy')
    scaredy_boy = Boy((200, 100), (-20, 0), 'scaredy boy')
    hungry_boy = Boy((200, 400), (20, 0), 'hungry boy')
    friendly_boy = Boy((400, 400), (20, 0), 'friendly boy')
    return [hungry_boy, friendly_boy, scaredy_boy, boy]


def initialise_boys(arena, method):
    if method == 'steering':
        the_boys = all_the_boys()
    elif method == 'pathfinding':
        the_boys = pathfinding_boy(arena)
    arena.add_screen_objects(the_boys)