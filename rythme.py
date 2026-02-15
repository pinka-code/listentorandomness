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

def generer_motif_rythmique_pour_role(duree_mesure, rng, role):
    """
    Génère un motif rythmique adapté au rôle musical.
    La somme des durées = durée mesure.
    """

    if role == "pad":
        # Une seule note longue
        return [duree_mesure]

    elif role == "basse":
        # Notes sur les temps forts
        # exemple 4/4 → 4 noires
        nb_temps = int(duree_mesure)
        return [1.0 for _ in range(nb_temps)]

    elif role == "harmonie":
        # demi-notes ou noires régulières
        if rng.random() < 0.5:
            return [duree_mesure / 2, duree_mesure / 2]
        else:
            nb = int(duree_mesure)
            return [1.0 for _ in range(nb)]

    elif role == "contrechant":
        # motif modéré
        return generer_motif_rythmique(duree_mesure, rng)

    elif role == "melodie":
        # plus mobile → subdivisions
        motif = []
        temps_restant = duree_mesure
        while temps_restant > 0:
            val = rng.choice([0.25, 0.5, 0.5, 1.0])
            if val > temps_restant:
                val = temps_restant
            motif.append(val)
            temps_restant -= val
        return motif

    else:
        return generer_motif_rythmique(duree_mesure, rng)

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
