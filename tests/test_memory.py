from screen_objects.wall import Wall
from brains.memory import Memory


def test_memory_stores_walls():
    wall = Wall((0, 0), (10, 0))
    memory = Memory()
    memory.remember_walls([wall])
    assert [i for i in memory.known_walls] == [wall]
