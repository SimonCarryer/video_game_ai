from screen_objects.boy import Boy
from screen_objects.item import Item
from item_manager.item_manager import ItemManager
from item_manager.customer_manager import CustomerManager
from brains.pathfinding.grid import BackgroundGrid
from util.helpers import walls_vector_from_game_objects


def pathfinding_boy(arena):
    hungry_boy = Boy((200, 400), (20, 0), 'pathfinding boy')
    hungry_boy.brain.goal_getter.intitialise_grid(arena, 24)
    return [hungry_boy]


def goap_boys(arena):
    #walls_vector = walls_vector_from_game_objects(arena.screen_objects)
    #grid = BackgroundGrid(arena.w, arena.h, 24)
    #grid.calculate_edges(walls_vector)
    shopkeeper = Boy((520, 520), (10, 0), 'shopkeeper')
    #customer = Boy((50, 105), (10, 0), 'customer')
    #customer.brain.goal_getter.intitialise_grid(grid)
    #customer2 = Boy((60, 130), (10, 0), 'customer')
    #customer2.brain.goal_getter.intitialise_grid(grid)
    return [shopkeeper]


def all_the_boys():
    boy = Boy((100, 105), (0, 0), 'tootling boy')
    scaredy_boy = Boy((200, 100), (-20, 0), 'scaredy boy')
    hungry_boy = Boy((200, 400), (20, 0), 'hungry boy')
    friendly_boy = Boy((400, 400), (20, 0), 'friendly boy')
    return [hungry_boy, friendly_boy, scaredy_boy, boy]


def initialise_boys(arena, method):
    if method == 'steering':
        the_boys = all_the_boys()
    elif method == 'pathfinding':
        the_boys = pathfinding_boy(arena)
    elif method == 'goap':
        the_boys = goap_boys(arena)
        arena.managers.append(CustomerManager(arena))
        arena.managers.append(ItemManager(arena))
    arena.add_screen_objects(the_boys)