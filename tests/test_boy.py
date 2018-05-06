from screen_objects.boy import Boy


def test_boy_is_cooked_from_recipe():
    boy = Boy((100, 100), (20, 0), 'tootling boy')
    assert boy.substance.radius == 7.5
    assert boy.sprite.colour == (0, 0, 220)
    assert boy.movement.max_accelleration == 2


def test_boy_has_unique_name():
    boy = Boy((100, 100), (20, 0), 'tootling boy')
    boy2 = Boy((100, 100), (20, 0), 'tootling boy')
    assert boy.name != boy2.name
