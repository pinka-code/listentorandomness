from phrase import Phrase

class Track:
    """
    Responsabilité :
    - Générer des phrases successives
    - Remplir l'instrument avec les notes produites
    - Respecter la durée totale du morceau
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

    def _generate_rhythm(self, size):
        return [1.0 for _ in range(size)]

    def generate(self):
        time = 0.0

        while time < self.config.total_duration:
            melodic_pattern = self._generate_pattern()
            rhythm = self._generate_rhythm(len(melodic_pattern))

            phrase = Phrase(
                config=self.config,
                melodic_pattern=melodic_pattern,
                rhythmic_pattern=rhythm,
                measure_count=1,
                role=self.role,
                measure_class=self.measure_class,
                rng=self.rng,
            )

            notes = phrase.play(start_time=time, velocity=80) #TODO config ici

            for note in notes:
                end_time = note.start + note.duration

                if end_time <= self.config.total_duration:
                    self.instrument.notes.append(note.to_midi())

            if notes:
                time = max(n.start + n.duration for n in notes)
            else:
                break
