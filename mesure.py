import octaves, rythme, nuances
import pretty_midi  # type: ignore

def calculer_duree_mesure(num, den):
    """
    Retourne la durée d'une mesure en beats MIDI standard
    """
    return num * (4 / den)

def construire_mesure(instr, mesure_start, duree_mesure, config, rng):
    """
    Remplit une mesure pour un instrument donné.
    
    - instr : PrettyMIDI Instrument
    - mesure_start : début de la mesure (en beats)
    - duree_mesure : durée totale de la mesure (en beats)
    - config : configuration globale du morceau
    - rng : générateur random personnalisé
    """
    time = mesure_start

    while time - mesure_start < duree_mesure:

        # silence aléatoire
        if rythme.generer_silence(rng):
            duration = rythme.choisir_duree(rng)
            if time + duration > mesure_start + duree_mesure:
                duration = mesure_start + duree_mesure - time
            time += duration
            continue

        # note aléatoire
        note_base = rng.choice(config.gamme_notes)
        octave = octaves.choisir_octave(rng)
        pitch = note_base + 12 * octave
        duration = rythme.choisir_duree(rng)
        if time + duration > mesure_start + duree_mesure:
            duration = mesure_start + duree_mesure - time

        velocity = nuances.choisir_nuance(rng)
        # accent simple sur temps fort
        if (time - mesure_start) % 1 == 0:
            velocity = min(127, velocity + 10)

        note = pretty_midi.Note(
            velocity=velocity,
            pitch=pitch,
            start=time,
            end=time + duration
        )
        instr.notes.append(note)
        time += duration

    return time  # fin de la mesure
