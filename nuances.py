# nuances.py
import random

NUANCES = {
    "PP": 10,    # Pianissimo, très doux
    "P": 30,     # Piano, calme
    "MP": 50,    # Mezzo-piano, normal
    "MF": 70,    # Mezzo-forte, standard
    "F": 90,     # Forte, accentué
    "FF": 110    # Fortissimo, très accentué
}

def choisir_nuance():
    """
    Retourne une valeur MIDI aléatoire correspondant à une nuance.
    """
    return random.choice(list(NUANCES.values()))

def choisir_nuance_avec_nom():
    """
    Retourne un tuple (nom, valeur) pour la nuance choisie aléatoirement.
    Utile pour debug ou affichage.
    """
    nom, valeur = random.choice(list(NUANCES.items()))
    return nom, valeur