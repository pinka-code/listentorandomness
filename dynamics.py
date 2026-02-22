DYNAMICS = {
    "PP": 10,    # Pianissimo, very soft
    "P": 30,     # Piano, soft
    "MP": 50,    # Mezzo-piano, moderate
    "MF": 70,    # Mezzo-forte, standard
    "F": 90,     # Forte, strong
    "FF": 110    # Fortissimo, very strong
}

def choose_dynamic(rng):
    """
    Returns a random MIDI value corresponding to a dynamic level.
    """
    return rng.choice(list(DYNAMICS.values()))