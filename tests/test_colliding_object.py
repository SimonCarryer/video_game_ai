from physics.colliding_object import Colliding


def test_colliding_object_gets_unique_name():
    obj_1 = Colliding((0, 0))
    obj_2 = Colliding((0, 0))
    assert obj_1.name != obj_2.name