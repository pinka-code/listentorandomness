import rythme, pretty_midi, orchestration, octaves, nuances

class Mesure:
    def __init__(self, motif, motif_rythmique, role, nom_instrument, config, rng):
        self.motif = motif
        self.motif_rythmique = motif_rythmique
        self.config = config
        self.rng = rng
        self.role = role
        self.nom_instrument = nom_instrument

    @staticmethod
    def calculer_duree(num, den):
        """
        Retourne la durée d'une mesure en beats MIDI standard
        """
        return num * (4 / den)
    
    def ajouter_tonique(self, instr, time_start, fraction_duree=0.5, nuance_phrase=None):
        """
        Ajoute une note finale résolvant sur la tonique.
        """
        note_base = self.config.notes_gamme[0]

        # octave via role si logique métier dépendante
        octave = self.role.choisir_octave(self)

        duree_mesure = self.calculer_duree(
            self.config.signature_num,
            self.config.signature_den
        )

        duration = duree_mesure * fraction_duree

        velocity = nuance_phrase if nuance_phrase is not None else nuances.choisir_nuance(self.rng)
        velocity = self.role.ajuster_velocity(velocity)
        velocity = max(20, min(127, velocity))

        pitch = note_base + 12 * octave
        pitch = orchestration.ajuster_pitch_au_registre(pitch, self.nom_instrument)

        note = pretty_midi.Note(
            velocity=velocity,
            pitch=pitch,
            start=time_start,
            end=time_start + duration
        )

        instr.notes.append(note)

        return time_start + duration

    def jouer(self, instr, time_start, nuance_phrase):
        time = time_start
        motif_idx = 0
        duree_mesure = sum(self.motif_rythmique)

        for duration in self.motif_rythmique:
            if rythme.generer_silence(self.rng, probabilite=0.1):
                time += duration
                continue

            pitch = self._calculer_pitch(motif_idx)
            duration = self._corriger_duree(time, time_start, duration, duree_mesure)

            if duration <= 0:
                break

            velocity = self._calculer_velocity(time, time_start, nuance_phrase)

            self._ajouter_note(instr, pitch, time, duration, velocity)

            time += duration
            motif_idx += 1

        return time
    
    def _calculer_pitch(self, motif_idx):
        degre = self.role.choisir_degre(self, motif_idx)
        note_base = self.config.notes_gamme[degre]

        octave = self.role.choisir_octave(self)

        pitch = note_base + 12 * octave
        pitch = orchestration.ajuster_pitch_au_registre(pitch, self.nom_instrument)

        return pitch
    
    def _corriger_duree(self, time, time_start, duration, duree_mesure):
        if time + duration > time_start + duree_mesure:
            duration = time_start + duree_mesure - time

        return duration
    
    def _calculer_velocity(self, time, time_start, nuance_phrase):
        velocity = nuance_phrase

        # accent temps fort
        if (time - time_start) % 1 == 0:
            velocity = min(127, velocity + 10)

        velocity = self.role.ajuster_velocity(velocity)

        return max(20, min(127, velocity))
    
    def _ajouter_note(self, instr, pitch, time, duration, velocity):
        note = pretty_midi.Note(
            pitch=pitch,
            start=time,
            end=time + duration,
            velocity=velocity
        )

        instr.notes.append(note)
