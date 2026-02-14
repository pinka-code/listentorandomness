import random

TEMPOS = {
    "LARGO": 50,       # très lent
    "ADAGIO": 70,      # lent
    "ANDANTE": 90,     # modéré, marche tranquille
    "MODERATO": 110,   # modéré
    "ALLEGRO": 130,    # rapide
    "PRESTO": 160      # très rapide
}

def choisir_tempo():
    """
    Retourne un tempo aléatoire (BPM) parmi TEMPOS
    """
    return random.choice(list(TEMPOS.values()))

def choisir_tempo_avec_nom():
    """
    Retourne un tuple (nom, BPM) pour le tempo choisi aléatoirement
    """
    nom, bpm = random.choice(list(TEMPOS.items()))
    return nom, bpm
