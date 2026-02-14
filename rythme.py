# rythme.py
import random

DUREES = {
    "QUADRUPLE_CROCHE": 0.125,
    "DOUBLE_CROCHE": 0.25,
    "CROCHE": 0.5,
    "CROCHE_POINTEE": 0.75,
    "NOIRE": 1.0,
    "NOIRE_POINTEE_CROCHE": 1.5,
    "BLANCHE": 2.0,
    "RONDE": 4.0
}

def choisir_duree():
    """
    Retourne une durée aléatoire (valeur en beats).
    Utilise les valeurs du dictionnaire DUREES.
    """
    return random.choice(list(DUREES.values()))

def choisir_duree_avec_nom():
    """
    Retourne un tuple (nom, valeur) pour la durée choisie aléatoirement.
    Utile pour debug ou affichage.
    """
    nom, valeur = random.choice(list(DUREES.items()))
    return nom, valeur

def generer_silence(probabilite=0.2):
    """
    Retourne True si on doit mettre un silence (probabilite 0..1)
    """
    return random.random() < probabilite