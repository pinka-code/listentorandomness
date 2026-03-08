from listener_to_randomness.midi.note import Note

class Phrase:
    """
    Responsibilities:
    - Orchestrate multiple measures
    - Apply melodic pattern variations
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

    def play(self, start_time: float):
        notes = []
        current_time = start_time
        current_pattern = self.melodic_pattern

        for i in range(self.measure_count):
            if i > 0 and self.rng.random() < self.config.phrase_variation_prob:
                current_pattern = current_pattern.transform(self.rng)

            rhythmic_pattern = self.role.generate_rhythm(
                self.config.measure_duration_quarters()
            )

            measure = self.measure_class(
                self.config,
                current_pattern,
                rhythmic_pattern,
                self.role,
            )

            notes.extend(
                measure.play(current_time, self.velocity)
            )

            current_time += rhythmic_pattern.total_duration()

        return notes
