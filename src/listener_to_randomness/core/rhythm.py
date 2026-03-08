DURATIONS = {
    "SIXTEENTH_NOTE": 0.125,
    "THIRTY_SECOND_NOTE": 0.25,
    "EIGHTH_NOTE": 0.5,
    "DOTTED_EIGHTH_NOTE": 0.75,
    "QUARTER_NOTE": 1.0,
    "DOTTED_QUARTER_NOTE_EIGHTH": 1.5,
    "HALF_NOTE": 2.0,
    "WHOLE_NOTE": 4.0
}

class RhythmicPattern:
    def __init__(self, pattern):
        self.pattern = pattern

    def total_duration(self):
        return sum(duration for duration, _ in self.pattern)

    @classmethod
    def generate(cls, total_beats, rng, rest_probability=0.0):
        pattern = []
        remaining = total_beats
        durations = list(DURATIONS.values())

        while remaining > 0:
            possible = [d for d in durations if d <= remaining]
            duration = rng.choice(possible)
            is_rest = rng.random() < rest_probability
            pattern.append((duration, is_rest))
            remaining -= duration

        return cls(pattern)

    def __iter__(self):
        return iter(self.pattern)

    def __len__(self):
        return len(self.pattern)