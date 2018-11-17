from brains.pathfinding.grid import BackgroundGrid
from screen_objects.boy import Boy
from util.helpers import walls_vector_from_game_objects
import random


class CustomerManager:
    def __init__(self, arena):
        self.arena = arena
        walls_vector = walls_vector_from_game_objects(arena.screen_objects)
        self.grid = BackgroundGrid(arena.w, arena.h, 24)
        self.grid.calculate_edges(walls_vector)
        self.counter = 0

    def make_customer(self):
        customer = Boy((50, 50), (0, 0), 'customer')
        customer.brain.goal_getter.intitialise_grid(self.grid)
        self.arena.add_screen_objects([customer])

    def update(self, list_of_game_objects):
        customers = [obj for obj in list_of_game_objects if obj.image.get('role') == 'customer']
        if len(customers) < 3:
            self.counter += 1
            if self.counter >= 50:
                self.counter = 0
                if random.randint(0, 2) == 1:
                    self.make_customer()
        for customer in customers:
            state = customer.brain.action_getter.interpreter.state
            if state['at_exit'] and state['got_item']:
                customer.delete = True
