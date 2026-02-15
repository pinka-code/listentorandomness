import octaves, rythme, nuances
import pretty_midi  # type: ignore

def construire_mesure_avec_motif(instr, mesure_start, duree_mesure, motif, config, rng, motif_rythmique=None, nuance_phrase=None):
    """
    Remplit une mesure en suivant un motif (liste de degrés) et un motif rythmique optionnel.
    Toutes les notes peuvent partager la même nuance si nuance_phrase est fournie.
    """
    if motif_rythmique is None:
        motif_rythmique = rythme.generer_motif_rythmique(duree_mesure, rng)

    time = mesure_start
    motif_idx = 0
    nb_notes_motif = len(motif)

    for duration in motif_rythmique:
        if rythme.generer_silence(rng, probabilite=0.1):
            time += duration
            if time > mesure_start + duree_mesure:
                time = mesure_start + duree_mesure
            continue

        degre = motif[motif_idx % nb_notes_motif]
        note_base = config.notes_gamme[degre]
        octave = octaves.choisir_octave(rng)

        if time + duration > mesure_start + duree_mesure:
            duration = mesure_start + duree_mesure - time

        accent = (time - mesure_start) % 1 == 0

        velocity = nuance_phrase if nuance_phrase is not None else nuances.choisir_nuance(rng)

        time = ajouter_note(
            instr,
            note_base,
            octave,
            time,
            duration,
            rng,
            accent=accent,
            velocity=velocity
        )

        motif_idx += 1
        if time >= mesure_start + duree_mesure:
            break

    return time

def ajouter_tonique(instr, time_start, config, rng, fraction_duree=0.5, nuance_phrase=None):
    """
    Ajoute une note finale résolvant la tonique à la fin d'une phrase ou d'une mesure.

    - instr : PrettyMIDI Instrument
    - time_start : temps de départ
    - config : configuration globale
    - rng : générateur random personnalisé
    - fraction_duree : fraction de la mesure à utiliser pour la note
    - nuance_phrase : vélocité à utiliser pour la phrase (facultatif)
    """

    note_base = config.notes_gamme[0]  
    octave = octaves.choisir_octave(rng)
    duree_mesure = calculer_duree_mesure(config.signature_num, config.signature_den)
    duration = duree_mesure * fraction_duree
    velocity = nuance_phrase if nuance_phrase is not None else nuances.choisir_nuance(rng)

    return ajouter_note(instr, note_base, octave, time_start, duration, rng, velocity=velocity)


def ajouter_note(instr, note_base, octave, start, duration, rng, accent=False, velocity=None):
    """
    Crée et ajoute une note à l'instrument.

    - instr : PrettyMIDI Instrument
    - note_base : note de base (degré dans la gamme)
    - octave : octave
    - start : temps de départ
    - duration : durée de la note
    - rng : générateur random
    - accent : si True, augmente légèrement la vélocité pour le temps fort
    """
    pitch = note_base + 12 * octave
    if velocity is None:
        velocity = nuances.choisir_nuance(rng)
    if accent:
        velocity = min(127, velocity + 10)

    note = pretty_midi.Note(
        velocity=velocity,
        pitch=pitch,
        start=start,
        end=start + duration
    )
    instr.notes.append(note)
    return start + duration

def calculer_duree_mesure(num, den):
    """
    Retourne la durée d'une mesure en beats MIDI standard
    """
    return num * (4 / den)
