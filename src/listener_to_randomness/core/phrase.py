from .measure import Measure

class Phrase:
    """
    Responsibilities:
    - Orchestrate multiple measures
    - Apply melodic pattern variations
    """

    def __init__(
        self,
        config,
        context,
        melodic_pattern,
        measure_count,
        role,
        velocity,
        rng,
    ):
        self.config = config
        self.context = context
        self.melodic_pattern = melodic_pattern
        self.measure_count = measure_count
        self.role = role
        self.velocity = velocity
        self.rng = rng

    def play(self, start_time: float):
        notes = []
        current_time = start_time
        current_melodic_pattern = self.melodic_pattern

        for i in range(self.measure_count):
            if i > 0 and self.rng.random() < self.config.phrase_variation_prob:
                current_melodic_pattern = current_melodic_pattern.transform(self.rng)

            current_rhythmic_pattern = self.role.generate_rhythm(self.context.measure_duration)
            
            measure = Measure(
                self.config,
                self.context,
                current_melodic_pattern,
                current_rhythmic_pattern,
                self.role,
            )

            notes.extend(
                measure.play(current_time, self.velocity)
            )

            current_time += current_rhythmic_pattern.total_duration()

        return notes
