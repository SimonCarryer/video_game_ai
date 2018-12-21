import random
from screen_objects.item import Item
from brains.action_planning.plan_interpreter import ACTION_BUS
from util.helpers import find_closest_point_index


class ItemManager:
    def __init__(self, arena):
        self.arena = arena
        self.h = arena.h
        self.w = arena.w

    def generate_item(self):
        if random.randint(0, 2) == 1: 
            x = random.randint(10, self.w - 10)
            y = random.randint(10, self.h - 10)
            colour = (100, 100, 100)
            item = Item((x, y), colour, radius=5.0)
            item.image['item type'] = 'shop'
        else: 
            item = self.generate_mess()
        return item

    def generate_mess(self):
        x = random.randint(10, self.w - 10)
        y = random.randint(10, self.h - 10)
        colour = (38, 75, 0)
        item = Item((x, y), colour, radius=10.0)
        item.image['item type'] = 'mess'
        return item

    def item_actions(self, actions, items):
        for action, coords in actions:
            if action.get('got_item') or action.get('mess_cleaned'):
                item_coords = [i.coords() for i in items]
                closest_item = items[find_closest_point_index(coords, item_coords)]
                closest_item.delete = True

    def update(self, list_of_game_objects):
        global ACTION_BUS
        items = [obj for obj in list_of_game_objects if obj.image.get('kind') == 'item']
        self.item_actions(ACTION_BUS, items)
        del ACTION_BUS[:]
        if len(items) < 3:
            item = self.generate_item()
            self.arena.add_screen_objects([item])

    
