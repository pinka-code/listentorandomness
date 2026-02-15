import instruments
from phrase import Phrase

def construire_morceau(midi, config, rng):
    """
    Construit toutes les pistes du morceau avec phrases et motifs.
    
    - midi : PrettyMIDI object
    - config : MusicConfig
    - rng : générateur random personnalisé
    """

    for piste_id in range(config.num_pistes):
        instr, famille = instruments.choisir_instrument(rng)
        print(f"Piste {piste_id+1} → {famille}")

        time = 0.0
        while time < config.duree_totale:
            phrase_obj = Phrase(config, rng)
            time = phrase_obj.jouer(instr, time)

    midi.instruments.append(instr)

