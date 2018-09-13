from screen_objects.boy import Boy
from screen_objects.wall import Wall


def test_boy_is_cooked_from_recipe():
    boy = Boy((100, 100), (20, 0), 'tootling boy')
    assert boy.body.substance.radius == 7.5
    assert boy.body.sprite.colour == (0, 0, 220)
    assert boy.body.movement.max_accelleration == 2


def test_boy_has_unique_name():
    boy = Boy((100, 100), (20, 0), 'tootling boy')
    boy2 = Boy((100, 100), (20, 0), 'tootling boy')
    assert boy.name != boy2.name


def test_initialise_frontal_lobe():
    boy = Boy((100, 100), (20, 0), 'pathfinding boy')
    wall = Wall((12, 12), (12, 32))
    wall2 = Wall((12, 12), (12, 14))
    boy.initialise_frontal_lobe(100, 100, [wall, wall2], grid_spacing=20)
    assert len(boy.brain.frontal_lobe.grid.graph.edges()) == 69

