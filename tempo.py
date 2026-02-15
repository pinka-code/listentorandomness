import rng

TEMPOS = {
    "LARGO": 50,       # très lent
    "ADAGIO": 70,      # lent
    "ANDANTE": 90,     # modéré, marche tranquille
    "MODERATO": 110,   # modéré
    "ALLEGRO": 130,    # rapide
    "PRESTO": 160      # très rapide
}

def choisir_tempo(rng):
    """
    Retourne un tempo aléatoire (BPM) parmi TEMPOS
    """
    return rng.choice(list(TEMPOS.values()))

def choisir_tempo_avec_nom(rng):
    """
    Retourne un tuple (nom, BPM) pour le tempo choisi aléatoirement
    """
    nom, bpm = rng.choice(list(TEMPOS.items()))
    return nom, bpm
