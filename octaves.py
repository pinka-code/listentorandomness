OCTAVES = {
    "OCTAVE_3": 3,
    "OCTAVE_4": 4,
    "OCTAVE_5": 5,
    "OCTAVE_6": 6
}

def choisir_octave(rng):
    """
    Retourne une octave aléatoire (valeur entière)
    """
    return rng.choice(list(OCTAVES.values()))
