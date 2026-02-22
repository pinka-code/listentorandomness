from enum import Enum

class Octave(Enum):
    OCTAVE_1 = 1
    OCTAVE_2 = 2
    OCTAVE_3 = 3
    OCTAVE_4 = 4
    OCTAVE_5 = 5
    OCTAVE_6 = 6

def choose_octave(rng, octaves=None):
    """
    Returns a random octave (integer value) among the given list of Octave Enum members.
    If no list is provided, choose among all octaves.
    """
    if octaves is None:
        octaves = list(Octave)
    return rng.choice([o.value for o in octaves])