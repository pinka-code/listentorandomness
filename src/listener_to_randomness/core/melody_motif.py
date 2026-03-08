def generate_pattern(config, rng):
    scale_len = len(config.scale_notes)

    length = rng.randint(
        config.pattern_length_min,
        config.pattern_length_max
    )

    degrees = list(range(scale_len))
    start_weights = [4 if d == 0 else 1 for d in degrees]

    current = rng.choice_weighted(degrees, weights=start_weights)
    motif = [current]

    interval_choices = [-2, -1, 0, 1, 2, 3, -3]
    interval_weights = [1, 4, 3, 4, 2, 1, 1]

    for _ in range(length - 1):
        interval = rng.choice_weighted(interval_choices, weights=interval_weights)
        current += interval
        motif.append(current)

    return motif

def transform_pattern(pattern, rng):
    transform = rng.choice([
        "transpose",
        "invert",
        "retrograde",
        "shift"
    ])

    if transform == "transpose":
        shift = rng.randint(-2, 2)
        return [p + shift for p in pattern]

    if transform == "invert":
        center = pattern[0]
        return [center - (p - center) for p in pattern]

    if transform == "retrograde":
        return list(reversed(pattern))

    if transform == "shift":
        k = rng.randint(1, len(pattern) - 1)
        return pattern[k:] + pattern[:k]

    return pattern