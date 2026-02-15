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

def choisir_duree(rng):
    """
    Retourne une durée aléatoire (valeur en beats).
    Utilise les valeurs du dictionnaire DUREES.
    """
    return rng.choice(list(DUREES.values()))

def generer_silence(rng, probabilite=0.2):
    """
    Retourne True si on doit mettre un silence (probabilite 0..1)
    """
    return rng.random() < probabilite

def generer_motif_rythmique(longueur_beats, rng):
    """
    Génère un motif rythmique pour une mesure ou une phrase.
    - longueur_beats : durée totale de la mesure/phrase en beats
    - rng : générateur random
    Retourne une liste de durées qui s'additionnent à longueur_beats
    """
    motif = []
    restant = longueur_beats

    while restant > 0:
        possibles = [v for v in DUREES.values() if v <= restant]
        d = rng.choice(possibles)
        motif.append(d)
        restant -= d

    return motif
