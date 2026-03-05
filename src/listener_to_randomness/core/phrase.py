from listener_to_randomness.midi.note import Note

class Phrase:
    """
    Responsibilities:
    - Orchestrate multiple measures
    - Apply melodic pattern variations
    - Add the final note
    """

    def __init__(
        self,
        config,
        melodic_pattern,
        measure_count,
        role,
        velocity,
        measure_class,
        rng,
    ):
        self.config = config
        self.melodic_pattern = melodic_pattern
        self.measure_count = measure_count
        self.role = role
        self.velocity = velocity
        self.measure_class = measure_class
        self.rng = rng

    def _change_pattern(self, motif):
        return [
            degre + self.rng.choice([-1, 0, 1])
            for degre in motif
        ]
    
    def _compute_measure_duration(self) -> float:
        """
        Compute measure duration in quarter-note units.
        (1.0 = quarter note)
        """
        num = self.config.time_signature_num
        den = self.config.time_signature_den

        return num * (4 / den)

    def _add_final_note(self, notes, velocity):
        pitch, fraction_duree = self.role.choose_final_note()

        last_time = max(n.start + n.duration for n in notes)

        notes.append(
            Note(
                pitch=pitch,
                start=last_time,
                duration=fraction_duree,
                velocity=velocity,
            )
        )

    def play(self, start_time: float):
        notes = []
        current_time = start_time
        current_pattern = self.melodic_pattern

        for i in range(self.measure_count):

            if i > 0 and self.rng.random() < self.config.phrase_variation_prob:
                current_pattern = self._change_pattern(current_pattern)

            measure_duration = self._compute_measure_duration()
            rhythmic_pattern = self.role.generate_rhythm(measure_duration)

            measure = self.measure_class(
                self.config,
                current_pattern,
                rhythmic_pattern,
                self.role,
            )

            measure_notes = measure.play(current_time, self.velocity)

            for note in measure_notes:
                jitter = (-0.125 + 0.25 * self.rng.random()) * note.duration
                note.start = max(0.0, note.start + jitter)

            notes.extend(measure_notes)

            measure_duration_sum = sum(
                dur if isinstance(dur, float) else dur[0] for dur in rhythmic_pattern
            )
            current_time += measure_duration_sum

        self._add_final_note(notes, self.velocity)

        return notes
