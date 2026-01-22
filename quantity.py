# standard library
from enum import IntEnum


class Quantity(IntEnum):
    """
    Enum for convenient/readable indexing of the main data matrix
    """

    SLEEP = 0
    MOOD = 1
    FOOD = 2
    HYDRATION = 3
    EXERCISE = 4
    SELFCARE = 5
    SOCIAL = 6
    STRESS = 7
    COUNT = 8
