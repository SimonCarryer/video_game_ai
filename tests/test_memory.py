from screen_objects.wall import Wall
from brains.memory import Memory
from mocks.mock_body_parts import MockBody, MockEyes


def test_memory_stores_walls():
    eyes = MockEyes()
    body = MockBody()
    wall = Wall((0, 0), (10, 0))
    memory = Memory(body, eyes)
    memory.remember_walls([wall])
    assert [i for i in memory.known_walls] == [wall]
