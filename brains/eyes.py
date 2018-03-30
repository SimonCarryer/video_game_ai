import pygame
import numpy as np


class Eyes:
    def __init__(self):
        pass

    def get_mouse_position(self):
        return np.array(pygame.mouse.get_pos()).astype(float)
