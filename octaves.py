# octaves.py
import random

OCTAVES = {
    "OCTAVE_3": 3,
    "OCTAVE_4": 4,
    "OCTAVE_5": 5,
    "OCTAVE_6": 6
}

def choisir_octave():
    """
    Retourne une octave aléatoire (valeur entière)
    """
    return random.choice(list(OCTAVES.values()))
