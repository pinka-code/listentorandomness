import octaves, rythme, nuances
import pretty_midi  # type: ignore

def calculer_duree_mesure(num, den):
    """
    Retourne la durée d'une mesure en beats MIDI standard
    """
    return num * (4 / den)

def ajouter_tonique(instr, time_start, config, rng, fraction_duree=0.5):
    """
    Ajoute une note finale résolvant la tonique à la fin d'une phrase ou d'une mesure.
    
    - instr : PrettyMIDI Instrument
    - time_start : temps de départ
    - config : configuration globale
    - rng : générateur random personnalisé
    - fraction_duree : fraction de la mesure à utiliser pour la note
    """

    # Tonique de la gamme / armature
    note_base = config.notes_gamme[0]  
    octave = octaves.choisir_octave(rng)
    pitch = note_base + 12 * octave

    # Durée : fraction de la mesure
    duree_mesure = calculer_duree_mesure(config.signature_num, config.signature_den)
    duration = duree_mesure * fraction_duree

    velocity = nuances.choisir_nuance(rng)

    note = pretty_midi.Note(
        velocity=velocity,
        pitch=pitch,
        start=time_start,
        end=time_start + duration
    )
    instr.notes.append(note)

    return time_start + duration

def construire_mesure_avec_motif(instr, mesure_start, duree_mesure, motif, config, rng):
    """
    Remplit une mesure en suivant un motif (liste de degrés).
    
    - instr : PrettyMIDI Instrument
    - mesure_start : début de la mesure (en beats)
    - duree_mesure : durée totale de la mesure (en beats)
    - motif : liste de degrés (indices dans config.notes_gamme)
    - config : configuration globale du morceau
    - rng : générateur random personnalisé
    """
    time = mesure_start
    motif_idx = 0
    nb_notes_motif = len(motif)

    while time - mesure_start < duree_mesure:

        # silence aléatoire
        if rythme.generer_silence(rng, probabilite=0.1):
            duration = rythme.choisir_duree(rng)
            if time + duration > mesure_start + duree_mesure:
                duration = mesure_start + duree_mesure - time
            time += duration
            continue

        # note selon le motif
        degre = motif[motif_idx % nb_notes_motif]
        note_base = config.notes_gamme[degre]

        octave = octaves.choisir_octave(rng)
        pitch = note_base + 12 * octave

        duration = rythme.choisir_duree(rng)
        if time + duration > mesure_start + duree_mesure:
            duration = mesure_start + duree_mesure - time

        velocity = nuances.choisir_nuance(rng)
        # accent sur le temps fort
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
        motif_idx += 1

    return time
