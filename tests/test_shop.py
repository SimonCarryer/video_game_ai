from screen_objects.boy import Boy


def test_shopkeeper_clean_messes():
    shopkeeper = Boy((520, 520), (10, 0), 'shopkeeper')
    print shopkeeper.brain.action_getter.interpreter.formulate_plan()
    shopkeeper.brain.action_getter.interpreter.state['can_see_mess'] = True
    print [i['name'] for i in shopkeeper.brain.action_getter.interpreter.formulate_plan()]
