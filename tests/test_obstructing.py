from physics.physical_object import Obstructing


def test_obstructing_constructs_collision():
    obstruction = Obstructing()
    collision = obstruction.collision((10, 0), 10)
    assert collision.keys() == ['avoid', 'intersection', 'name']