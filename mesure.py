import octaves, rythme, pretty_midi, nuances
from orchestration import ajuster_pitch_au_registre

class Mesure:
    def __init__(self, motif, motif_rythmique, role, nom_instrument, config, rng):
        self.motif = motif
        self.motif_rythmique = motif_rythmique
        self.config = config
        self.rng = rng
        self.role = role
        self.nom_instrument = nom_instrument

    def jouer(self, instr, time_start, nuance_phrase):
        time = time_start
        motif_idx = 0
        for duration in self.motif_rythmique:
            # silence aléatoire
            if rythme.generer_silence(self.rng, probabilite=0.1):
                time += duration
                continue

            if self.role == "basse":
                # privilégie tonique et quinte
                degre = self.rng.choice([0, 4])

            elif self.role == "harmonie":
                # privilégie notes stables
                degre = self.rng.choice([0, 2, 4])

            else:
                # comportement normal
                degre = self.motif[motif_idx % len(self.motif)]

            note_base = self.config.notes_gamme[degre]
            
            if self.role == "basse":
                octave = self.rng.choice([1, 2])

            elif self.role == "melodie":
                octave = self.rng.choice([4, 5])

            elif self.role == "contrechant":
                octave = self.rng.choice([3, 4])

            elif self.role == "pad":
                octave = self.rng.choice([3, 4])

            else:
                octave = self.rng.choice([3, 4])


            pitch = note_base + 12 * octave
            pitch = ajuster_pitch_au_registre(pitch, self.nom_instrument)

            # ajuster durée si dépassement mesure
            duree_mesure = sum(self.motif_rythmique)
            if time + duration > time_start + duree_mesure:
                duration = time_start + duree_mesure - time
            if duration <= 0:
                break

            velocity = nuance_phrase
            if (time - time_start) % 1 == 0:  # accent sur temps fort
                velocity = min(127, velocity + 10)

            if self.role == "melodie":
                velocity += 10

            elif self.role == "basse":
                velocity += 5

            elif self.role == "pad":
                velocity -= 10

            velocity = max(20, min(127, velocity))

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