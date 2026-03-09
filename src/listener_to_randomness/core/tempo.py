TEMPOS = {
    "LARGO": 50,       # very slow
    "ADAGIO": 70,      # slow
    "ANDANTE": 90,     # moderate, walking pace
    "MODERATO": 110,   # moderate
    "ALLEGRO": 130,    # fast
    "PRESTO": 160      # very fast
}

def choose(rng):
    """
    Returns a random tempo (BPM) from TEMPOS.
    """
    return rng.choice(list(TEMPOS.values()))
