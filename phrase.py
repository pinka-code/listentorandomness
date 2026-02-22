from note import Note

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
        rhythmic_pattern,
        measure_count,
        role,
        measure_class,
        rng,
    ):
        self.config = config
        self.melodic_pattern = melodic_pattern
        self.rhythmic_pattern = rhythmic_pattern
        self.measure_count = measure_count
        self.role = role
        self.measure_class = measure_class
        self.rng = rng

    def _change_pattern(self, motif):
        return [
            degre + self.rng.choice([-1, 0, 1])
            for degre in motif
        ]

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

    def play(self, start_time: float, velocity: int):
        notes = []
        current_time = start_time
        current_pattern = self.melodic_pattern

        for i in range(self.measure_count):

            if i > 0 and self.rng.random() < self.config.phrase_variation_prob:
                current_pattern = self._change_pattern(current_pattern)

            measure = self.measure_class(
                self.config,
                current_pattern,
                self.melodic_pattern,
                self.role,
            )

            measure_notes = measure.play(current_time, velocity)

            notes.extend(measure_notes)

            measure_duration = sum(n.duration for n in measure_notes)
            current_time += measure_duration

        self._add_final_note(notes, velocity)

        return notes
