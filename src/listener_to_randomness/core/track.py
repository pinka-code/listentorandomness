from .phrase import Phrase
from . import dynamics

class Track:

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

        self.section_themes = {}

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
            interval = self.rng.choice_weighted(
                interval_choices,
                weights=interval_weights
            )

            current = current + interval
            motif.append(current)

        return motif
    
    def _transform_pattern(self, pattern):
        transform = self.rng.choice([
            "transpose",
            "invert",
            "retrograde",
            "shift"
        ])

        if transform == "transpose":
            shift = self.rng.randint(-2, 2)
            return [p + shift for p in pattern]

        if transform == "invert":
            center = pattern[0]
            return [center - (p - center) for p in pattern]

        if transform == "retrograde":
            return list(reversed(pattern))

        if transform == "shift":
            k = self.rng.randint(1, len(pattern) - 1)
            return pattern[k:] + pattern[:k]

        return pattern

    def _pattern_for_section(self, section_name):
        if section_name in self.section_themes:
            return self.section_themes[section_name]

        if section_name == "A":
            pattern = self._generate_pattern()

        else:
            base = self.section_themes.get("A")
            if base:
                pattern = self._transform_pattern(base)
            else:
                pattern = self._generate_pattern()

        self.section_themes[section_name] = pattern

        return pattern

    def generate_section(self, section, start_bar):
        bar_duration = section.bar_duration(self.config)
        start_time = start_bar * bar_duration
        end_time = start_time + section.bars * bar_duration
        time = start_time
        melodic_pattern = self._pattern_for_section(section.name)

        while time < end_time:

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
                note_end = note.start + note.duration

                if note_end <= end_time:
                    self.instrument.notes.append(note.to_midi())

            if notes:
                time = max(n.start + n.duration for n in notes)
            else:
                break
