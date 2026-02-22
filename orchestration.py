import pretty_midi  # type: ignore
from instruments import INSTRUMENTS

ROLES = [
    "melody",
    "countermelody",
    "harmony",
    "bass",
    "pad"
]

ORCHESTRATION = {
    "melody": ["Violin", "Flute", "Oboe", "Clarinet", "Trumpet"],
    "countermelody": ["Viola", "Clarinet", "French Horn"],
    "harmony": ["Acoustic Grand Piano", "String Ensemble 1", "Church Organ"],
    "bass": ["Cello", "Contrabass", "Electric Bass (finger)", "Acoustic Bass"],
    "pad": ["Pad 1 (new age)", "String Ensemble 1"]
}

RANGES = {
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

def choose_instrument_for_role(rng, role):
    name = rng.choice(ORCHESTRATION[role])
    program = INSTRUMENTS[name]
    instrument = pretty_midi.Instrument(program=program)
    return instrument, name
