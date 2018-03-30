import numpy as np
from brains.hindbrain import Hindbrain


def test_calculate_vector_to_target_returns_correct_vector():
    lizard_brain = Hindbrain()
    current = np.array((10.0, 10.0))
    target = np.array((20.0, 10.0))
    vector = lizard_brain.calculate_vector_to_target(current, target)
    assert (vector == (1, 0)).all()