DURATIONS = {
    "THIRTY_SECOND_NOTE": 0.125,
    "SIXTEENTH_NOTE": 0.25,
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
    def generate(cls, total_beats, rng, rest_probability=0.0, time_signature=None, syncopation_prob=0.2):
        pattern = []
        remaining = total_beats
        beat_position = 0.0  # track position within the measure for syncopation

        durations = list(DURATIONS.values())

        base_weights = {
            0.125: 0.1, 0.25: 0.2, 0.5: 1.0, 0.75: 0.5,
            1.0: 1.0, 1.5: 0.3, 2.0: 0.2, 4.0: 0.1
        }

        # Adjust weights based on signature
        if time_signature is not None:
            if time_signature.type == "binary":
                for d in base_weights:
                    if d <= 1.0:
                        base_weights[d] *= 1.0
                    else:
                        base_weights[d] *= 0.3
            elif time_signature.type == "ternary":
                for d in base_weights:
                    if 0.5 <= d <= 1.5:
                        base_weights[d] *= 1.0
                    else:
                        base_weights[d] *= 0.2

        while remaining > 0:
            possible = [d for d in durations if d <= remaining]
            if not possible:
                break
            possible_weights = [base_weights[d] for d in possible]

            if time_signature is not None and rng.random() < syncopation_prob:
                if time_signature.type == "binary" and (beat_position % 1.0 != 0):
                    possible_weights = [w * 1.5 if d <= 0.5 else w for d, w in zip(possible, possible_weights)]
                elif time_signature.type == "ternary" and (beat_position % 1.5 != 0):
                    possible_weights = [w * 1.5 if d <= 0.5 else w for d, w in zip(possible, possible_weights)]

            duration = rng.choice_weighted(possible, possible_weights)
            is_rest = rng.random() < rest_probability
            pattern.append((duration, is_rest))
            remaining -= duration
            beat_position += duration

        return cls(pattern)

    def __iter__(self):
        return iter(self.pattern)

    def __len__(self):
        return len(self.pattern)