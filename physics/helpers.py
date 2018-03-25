import numpy as np
from sklearn.preprocessing import normalize


def normalise_vector(vector):
    return normalize(vector.reshape(1, -1))[0]


def magnitude_vector(vector):
    return np.linalg.norm(vector)
