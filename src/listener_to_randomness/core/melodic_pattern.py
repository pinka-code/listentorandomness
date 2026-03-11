from listener_to_randomness.utils.music_profiles import merge_profiles

class MelodicPattern:

    def __init__(self, degrees):
        self.degrees = degrees

    def transform(self, rng):
        transform = rng.choice([
            "transpose",
            "invert",
            "retrograde",
            "shift",
            "none"
        ])

        pattern = self.degrees

        if transform == "transpose":
            shift = rng.randint(-2, 2)
            return MelodicPattern([p + shift for p in pattern])

        if transform == "invert":
            center = pattern[0]
            return MelodicPattern([
                center - (p - center)
                for p in pattern
            ])

        if transform == "retrograde":
            return MelodicPattern(list(reversed(pattern)))

        if transform == "shift":
            if len(pattern) <= 1:
                return MelodicPattern(pattern)

            k = rng.randint(1, len(pattern) - 1)
            return MelodicPattern(pattern[k:] + pattern[:k])

        return MelodicPattern(pattern)
    
    @classmethod
    def generate(cls, context, rng, role=None):
        style = context.style
        style_profile = style.melodic_profile
        role_profile = role.melodic_profile if role else {}

        profile = merge_profiles(style_profile, role_profile)

        scale_len = len(context.scale_notes)

        length = rng.randint(
            style.pattern_length_min,
            style.pattern_length_max
        )

        degrees = list(range(scale_len))

        start_weights = [
            profile.get("start_degree_weight", {}).get(d, 1)
            for d in degrees
        ]

        current = rng.choice_weighted(degrees, weights=start_weights)
        motif = [current]

        interval_choices = profile["intervals"]
        interval_weights = profile["weights"]

        for _ in range(length - 1):
            interval = rng.choice_weighted(
                interval_choices,
                weights=interval_weights
            )

            current += interval
            motif.append(current)

        return cls(motif)
