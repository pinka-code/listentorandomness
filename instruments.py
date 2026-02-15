import pretty_midi # type: ignore

INSTRUMENTS = {
    "Piano": range(0, 8),
    "Chromatic_Percussion": range(8, 16),
    "Organ": range(16, 24),
    "Guitar": range(24, 32),
    "Bass": range(32, 40),
    "Strings": range(40, 48),
    "Ensemble": range(48, 56),
    "Brass": range(56, 64),
    "Reed": range(64, 72),
    "Pipe": range(72, 80),
    "Synth_Lead": range(80, 88),
    "Synth_Pad": range(88, 96),
    "Synth_Effects": range(96, 104),
    "Ethnic": range(104, 112),
    "Percussive": range(112, 120),
    "Sound_Effects": range(120, 128)
}

def choisir_instrument(rng):
    """
    Retourne un objet Instrument aléatoire choisi dans une famille.
    Choisit d'abord une famille, puis un instrument dans la plage.
    """
    # Choisir une famille aléatoire
    famille, plage = rng.choice(list(INSTRUMENTS.items()))
    
    # Choisir un instrument dans cette famille
    instrument_num = rng.choice(list(plage))
    
    # Créer l'objet PrettyMIDI Instrument
    instrument = pretty_midi.Instrument(program=instrument_num)
    
    return instrument, famille