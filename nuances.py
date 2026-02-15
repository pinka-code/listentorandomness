NUANCES = {
    "PP": 10,    # Pianissimo, très doux
    "P": 30,     # Piano, calme
    "MP": 50,    # Mezzo-piano, normal
    "MF": 70,    # Mezzo-forte, standard
    "F": 90,     # Forte, accentué
    "FF": 110    # Fortissimo, très accentué
}

def choisir_nuance(rng):
    """
    Retourne une valeur MIDI aléatoire correspondant à une nuance.
    """
    return rng.choice(list(NUANCES.values()))
