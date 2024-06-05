from enum import Enum

class Bezier(Enum):
    LINEAR = (0, 0, 1, 1)
    EASE = (0.25, 0.1, 0.25, 1)
    EASE_IN = (0.42, 0, 1, 1)
    EASE_OUT = (0, 0, 0.58, 1)
    EASE_IN_OUT = (0.42, 0, 0.58, 1)
