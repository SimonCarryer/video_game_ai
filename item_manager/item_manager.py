import random
from screen_objects.item import Item


class ItemManager:
    def __init__(self, arena):
        self.arena = arena
        self.h = arena.h
        self.w = arena.w

    def generate_item(self):
        x = random.randint(10, self.w - 10)
        y = random.randint(10, self.h - 10)
        colour = (100, 100, 100)
        item = Item((x, y), colour)
        return item

    def update(self, list_of_game_objects):
        items = [obj for obj in list_of_game_objects if obj.image.get('kind') == 'item']
        if len(items) == 0:
            item = self.generate_item()
            self.arena.add_screen_objects([item])

    
