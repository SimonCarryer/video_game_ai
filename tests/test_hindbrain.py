import numpy as np
from brains.hindbrain import Hindbrain
from util.helpers import *


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


def test_calculate_vector_to_target_adds_avoid_vector():
    lizard_brain = Hindbrain()
    current = np.array((10.0, 10.0))
    target = np.array((20.0, 10.0))
    velocity = np.array((0.0, 0.0))
    collision = {'avoid': np.array((0.0, 1.0)),
                 'intersection': np.array((11.0, 10.0))}
    vector = lizard_brain.calculate_vector_to_target(current,
                                                     velocity,
                                                     target,
                                                     collision=collision)
    desired = normalise_vector(np.array((1.0, 1.0)))
    assert (vector == desired).all()


def test_calculate_vector_to_target_ignores_collisions_behind_target():
    lizard_brain = Hindbrain()
    current = np.array((10.0, 10.0))
    target = np.array((20.0, 10.0))
    velocity = np.array((0.0, 0.0))
    collision = {'avoid': np.array((0.0, 1.0)),
                 'intersection': np.array((21.0, 10.0))}
    vector = lizard_brain.calculate_vector_to_target(current,
                                                     velocity,
                                                     target,
                                                     collision=collision)
    desired = np.array((1.0, 0.0))
    assert (vector == desired).all()


