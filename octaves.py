OCTAVES = {
    "OCTAVE_3": 3,
    "OCTAVE_4": 4,
    "OCTAVE_5": 5,
    "OCTAVE_6": 6
}

def choose_octave(rng):
    """
    Returns a random octave (integer value).
    """
    return rng.choice(list(OCTAVES.values()))