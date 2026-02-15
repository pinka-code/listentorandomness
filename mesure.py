import octaves, rythme, pretty_midi, nuances

class Mesure:
    def __init__(self, motif, motif_rythmique, config, rng):
        self.motif = motif
        self.motif_rythmique = motif_rythmique
        self.config = config
        self.rng = rng

    def jouer(self, instr, time_start, nuance_phrase):
        time = time_start
        motif_idx = 0
        nb_notes = len(self.motif)
        for duration in self.motif_rythmique:
            # silence aléatoire
            if rythme.generer_silence(self.rng, probabilite=0.1):
                time += duration
                continue

            degre = self.motif[motif_idx % nb_notes]
            note_base = self.config.notes_gamme[degre]
            octave = octaves.choisir_octave(self.rng)
            pitch = note_base + 12 * octave

            # ajuster durée si dépassement mesure
            duree_mesure = sum(self.motif_rythmique)
            if time + duration > time_start + duree_mesure:
                duration = time_start + duree_mesure - time

            velocity = nuance_phrase
            if (time - time_start) % 1 == 0:  # accent sur temps fort
                velocity = min(127, velocity + 10)

            note = pretty_midi.Note(
                pitch=pitch,
                start=time,
                end=time + duration,
                velocity=velocity
            )
            instr.notes.append(note)
            time += duration
            motif_idx += 1
        return time

def calculer_duree(num, den):
    """
    Retourne la durée d'une mesure en beats MIDI standard
    """
    return num * (4 / den)

def ajouter_tonique(instr, time_start, config, rng, fraction_duree=0.5, nuance_phrase=None):
    """
    Ajoute une note finale résolvant la tonique à la fin d'une phrase ou d'une mesure.
    """
    note_base = config.notes_gamme[0]  # tonique
    octave = octaves.choisir_octave(rng)
    duree_mesure = calculer_duree(config.signature_num, config.signature_den)
    duration = duree_mesure * fraction_duree

    # velocity durable si fourni
    velocity = nuance_phrase if nuance_phrase is not None else nuances.choisir_nuance(rng)

    note = pretty_midi.Note(
        velocity=velocity,
        pitch=note_base + 12 * octave,
        start=time_start,
        end=time_start + duration
    )
    instr.notes.append(note)
    return time_start + duration