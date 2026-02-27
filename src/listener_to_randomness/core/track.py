from .phrase import Phrase
from . import dynamics

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
        scale_len = len(self.config.scale_notes)

        length = self.rng.randint(
            self.config.pattern_length_min,
            self.config.pattern_length_max
        )

        degrees = list(range(scale_len))
        start_weights = [4 if d == 0 else 1 for d in degrees]

        current = self.rng.choice_weighted(degrees, weights=start_weights)
        motif = [current]

        interval_choices = [-2, -1, 0, 1, 2, 3, -3]
        interval_weights = [1, 4, 3, 4, 2, 1, 1]

        for _ in range(length - 1):
            interval = self.rng.choice_weighted(interval_choices, weights=interval_weights)
            current = current + interval
            motif.append(current)

        return motif

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
