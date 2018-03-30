import numpy as np
from util.helpers import *


def test_normalise_vector():
    assert (normalise_vector(np.array([10.0, 0.0])) == [1, 0]).all()
    assert (normalise_vector(np.array([0.0, 6.6])) == [0, 1]).all()
    a = normalise_vector(np.array([9.0, 9.0]))
    b = normalise_vector(np.array([3.0, 3.0]))
    assert (a == b).all()


def test_distance_to_target():
    current = np.array([0.0, 0.0])
    desired = np.array([10.0, 0.0])
    assert distance_to_target(current, desired) == 10.0