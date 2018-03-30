import numpy as np
from brains.hindbrain import Hindbrain


def test_calculate_vector_to_target_returns_correct_vector():
    lizard_brain = Hindbrain()
    current = np.array((10.0, 10.0))
    target = np.array((20.0, 10.0))
    velocity = np.array((0.0, 0.0))
    vector = lizard_brain.calculate_vector_to_target(current, velocity, target)
    assert (vector == (1, 0)).all()


def test_calculate_vector_to_target_reduces_vector_for_close_targets():
    lizard_brain = Hindbrain()
    current = np.array((10.0, 10.0))
    target = np.array((12.0, 10.0))
    velocity = np.array((0.0, 0.0))
    vector = lizard_brain.calculate_vector_to_target(current, velocity, target)
    assert vector[0] == 0.4
    target = np.array((11.0, 10.0))
    vector = lizard_brain.calculate_vector_to_target(current, velocity, target)
    assert vector[0] == 0.2
