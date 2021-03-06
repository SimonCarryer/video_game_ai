from copy import deepcopy

boy_recipes = {}

boy_recipes['tootling boy'] = {
    'kind': 'boy',
    'radius': 7.5,
    'colour': (0, 0, 220),
    'behaviour': {},
    'accelleration': 2
}

boy_recipes['pathfinding boy'] = {
    'kind': 'boy',
    'radius': 8,
    'colour': (220, 0, 0),
    'behaviour': {'target': 'mouse pointer', 
                  'target behaviour': 'seek', 
                  'pathfind': True},
    'accelleration': 4
}

boy_recipes['patrol boy'] = {
    'kind': 'boy',
    'radius': 8,
    'colour': (220, 0, 0),
    'behaviour': {'plan_file': 'brains/action_planning/plan_files/patrol.json',
                  'start': {"at_point_1": False, "at_point_2": False, "at_point_3": False, "at_point_4": False},
                  'priorities': ["get_item", "complete_patrol"],
                  'target range': 150,
                  'goap': True},
    'accelleration': 4
}

boy_recipes['customer'] = {
    'kind': 'boy',
    'role': 'customer',
    'radius': 6,
    'colour': (200, 100, 0),
    'behaviour': {'plan_file': 'brains/action_planning/plan_files/shop.json',
                  'start': {"can_see_item": False, 
                            "at_exit": False, 
                            'got_item': False,
                            'close_to_item': False, 
                            'paid_for_item': False},
                  'priorities': ["buy_item"],
                  'target range': 500,
                  'goap': True,
                  'fast pathfind': True},
    'accelleration': 1
}

boy_recipes['shopkeeper'] = {
    'kind': 'boy',
    'role': 'shopkeeper',
    'radius': 8,
    'colour': (220, 0, 0),
    'behaviour': {'plan_file': 'brains/action_planning/plan_files/shop.json',
                  'start': {"can_see_item": False, 
                            "at_exit": False, 
                            'got_item': True, 
                            'paid_for_item': False,
                            'can_see_mess': False,
                            'close_to_mess': False,
                            'mess_cleaned': False},
                  'priorities': ["sell_item", "clean_messes"],
                  'target range': 500,
                  'goap': True,
                  'fast pathfind': True},
    'accelleration': 2
}


boy_recipes['hungry boy'] = {
    'kind': 'boy',
    'radius': 8,
    'colour': (220, 0, 0),
    'behaviour': {'target': 'mouse pointer', 
                  'target behaviour': 'seek', 
                  'pathfind': False},
    'accelleration': 4
}

boy_recipes['friendly boy'] = {
    'kind': 'boy',
    'radius': 7.5,
    'colour': (100, 100, 0),
    'behaviour': {'target': {'kind': 'boy'}, 'target range': 300, 'target behaviour': 'seek'},
    'accelleration': 1
}

boy_recipes['scaredy boy'] = {
    'kind': 'boy',
    'radius': 7.5,
    'colour': (0, 100, 100),
    'behaviour': {'target': {'kind': 'boy'}, 'target range': 100, 'target behaviour': 'flee'},
    'accelleration': 1.5
}


class CookBook:
    def __init__(self, recipes):
        self.recipes = recipes

    def get_recipe(self, recipe_name):
        return deepcopy(self.recipes[recipe_name])

boy_cookbook = CookBook(boy_recipes)