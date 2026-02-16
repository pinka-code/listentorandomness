import pretty_midi # type: ignore
from instruments import INSTRUMENTS

ROLES = [
    "melodie",
    "contrechant",
    "harmonie",
    "basse",
    "pad"
]

ORCHESTRATION = {
    "melodie": ["Violin", "Flute", "Oboe", "Clarinet", "Trumpet"],
    "contrechant": ["Viola", "Clarinet", "French Horn"],
    "harmonie": ["Acoustic Grand Piano", "String Ensemble 1", "Church Organ"],
    "basse": ["Cello", "Contrabass", "Electric Bass (finger)", "Acoustic Bass"],
    "pad": ["Pad 1 (new age)", "String Ensemble 1"]
}

REGISTRES = {
    "Violin": (55, 103),
    "Viola": (48, 88),
    "Cello": (36, 76),
    "Contrabass": (28, 60),

    "Flute": (60, 96),
    "Oboe": (58, 91),
    "Clarinet": (50, 94),
    "Bassoon": (34, 75),

    "Trumpet": (55, 82),
    "French Horn": (40, 80),
    "Trombone": (40, 72),
    "Tuba": (28, 55),

    "Acoustic Grand Piano": (21, 108),
    "String Ensemble 1": (40, 100),
    "Pad 1 (new age)": (48, 84),

    "Electric Bass (finger)": (28, 60),
    "Acoustic Bass": (28, 60),
}

def choisir_instrument_pour_role(rng, role):
    nom = rng.choice(ORCHESTRATION[role])
    programme = INSTRUMENTS[nom]
    instrument = pretty_midi.Instrument(program=programme)
    return instrument, nom

def ajuster_pitch_au_registre(pitch, instrument_name):
    if instrument_name not in REGISTRES:
        return pitch

    bas, haut = REGISTRES[instrument_name]

    while pitch < bas:
        pitch += 12
    while pitch > haut:
        pitch -= 12

    return pitch
