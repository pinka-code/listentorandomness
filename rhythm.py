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

def generate_rest(rng, probability=0.2):
    return rng.random() < probability

def generate_rhythmic_pattern(total_beats, rng, rest_probability=0.0):
    """
    Returns a list of tuples:
    [(duration, is_rest), ...]
    """
    pattern = []
    remaining = total_beats

    while remaining > 0:
        possible = [v for v in DURATIONS.values() if v <= remaining]
        duration = rng.choice(possible)

        is_rest = generate_rest(rng, rest_probability)

        pattern.append((duration, is_rest))
        remaining -= duration

    return pattern