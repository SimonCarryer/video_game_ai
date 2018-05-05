from copy import copy

boy_recipes = {}

boy_recipes['tootling boy'] = {
    'kind': 'tootling boy',
    'radius': 7.5,
    'colour': (0, 0, 220),
    'behaviour': {},
    'accelleration': 2
}

boy_recipes['hungry boy'] = {
    'kind': 'hungry boy',
    'radius': 8,
    'colour': (220, 0, 0),
    'behaviour': {'target': 'mouse pointer', 'target behaviour': 'seek'},
    'accelleration': 4
}

boy_recipes['friendly boy'] = {
    'kind': 'friendly boy',
    'radius': 7.5,
    'colour': (100, 100, 0),
    'behaviour': {'target': {'kind': 'hungry boy'}, 'target range': 300, 'target behaviour': 'seek'},
    'accelleration': 1
}

boy_recipes['scaredy boy'] = {
    'kind': 'scaredy boy',
    'radius': 7.5,
    'colour': (0, 100, 100),
    'behaviour': {},
    'accelleration': 1.5
}


class CookBook:
    def __init__(self, recipes):
        self.recipes = recipes

    def get_recipe(self, recipe_name):
        return copy(self.recipes[recipe_name])

boy_cookbook = CookBook(boy_recipes)