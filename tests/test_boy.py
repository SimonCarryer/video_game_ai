from screen_objects.boy import Boy


def test_boy_is_created_with_correct_attributes():
    boy = Boy((100, 100), (20, 0), 'tootling boy')
    assert boy.__dict__.keys() == ['brain', 'substance', 'sprite', 'movement']


def test_boy_is_cooked_from_recipe():
    boy = Boy((100, 100), (20, 0), 'tootling boy')
    assert boy.substance.radius == 7.5
    assert boy.brain.get_goal_vector.__name__ == 'wander'
    assert boy.sprite.colour == (0, 0, 220)
    assert boy.movement.max_accelleration == 2
