SIGNATURES = {
    "2/4": {"num": 2, "den": 4, "type": "binaire"},
    "3/4": {"num": 3, "den": 4, "type": "binaire"},
    "4/4": {"num": 4, "den": 4, "type": "binaire"},
    "2/2": {"num": 2, "den": 2, "type": "binaire"},
    "6/8": {"num": 6, "den": 8, "type": "ternaire"},
    "9/8": {"num": 9, "den": 8, "type": "ternaire"},
    "12/8": {"num": 12, "den": 8, "type": "ternaire"},
}

def choisir_signature(rng):
    """
    Retourne :
    - nom (ex: "4/4")
    - numerateur
    - denominateur
    - type ("binaire" ou "ternaire")
    """
    nom, data = rng.choice(list(SIGNATURES.items()))
    return nom, data["num"], data["den"], data["type"]
