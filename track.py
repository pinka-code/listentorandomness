from phrase import Phrase
import dynamics

class Track:
    """
    Responsibilities:
    - Generate successive phrases
    - Fill the instrument with the produced notes
    - Respect the total duration of the composition
    """

    def __init__(
        self,
        config,
        rng,
        role,
        instrument,
        instrument_name,
        measure_class,
    ):
        self.config = config
        self.rng = rng
        self.role = role
        self.instrument = instrument
        self.instrument_name = instrument_name
        self.measure_class = measure_class

    def _generate_pattern(self):
        return [
            self.rng.randint(0, len(self.config.scale_notes) - 1)
            for _ in range(self.rng.randint(
                self.config.phrase_length_min,
                self.config.phrase_length_max
            ))
        ]

    def generate(self):
        time = 0.0

        while time < self.config.total_duration:
            melodic_pattern = self._generate_pattern()
            velocity = dynamics.choose_dynamic(self.rng)
            measure_count = self.role.phrase_length()

            phrase = Phrase(
                config=self.config,
                melodic_pattern=melodic_pattern,
                measure_count=measure_count,
                role=self.role,
                velocity=velocity,
                measure_class=self.measure_class,
                rng=self.rng,
            )

            notes = phrase.play(start_time=time)

            for note in notes:
                end_time = note.start + note.duration

                if end_time <= self.config.total_duration:
                    self.instrument.notes.append(note.to_midi())

            if notes:
                time = max(n.start + n.duration for n in notes)
            else:
                break
