from orchestration import Role

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

def choose_duration(rng):
    """
    Returns a random duration (value in beats).
    Uses values from the DURATIONS dictionary.
    """
    return rng.choice(list(DURATIONS.values()))

def generate_rest(rng, probability=0.2):
    """
    Returns True if a rest should be inserted (probability 0..1).
    """
    return rng.random() < probability

def generate_rhythmic_pattern_for_role(measure_duration, rng, role):
    """
    Generates a rhythmic pattern adapted to the musical role.
    The sum of durations equals the measure duration.
    """

    if role == Role.PAD:
        # Single long note
        return [measure_duration]

    elif role == Role.BASS:
        # Notes on strong beats
        # example 4/4 → 4 quarter notes
        beats = int(measure_duration)
        return [1.0 for _ in range(beats)]

    elif role == Role.HARMONY:
        # Half notes or regular quarter notes
        if rng.random() < 0.5:
            return [measure_duration / 2, measure_duration / 2]
        else:
            beats = int(measure_duration)
            return [1.0 for _ in range(beats)]

    elif role == Role.COUNTERMELODY:
        # Moderate pattern
        return generate_rhythmic_pattern(measure_duration, rng)

    elif role == Role.MELODY:
        # More movement → subdivisions
        pattern = []
        remaining = measure_duration
        while remaining > 0:
            value = rng.choice([0.25, 0.5, 0.5, 1.0])
            if value > remaining:
                value = remaining
            pattern.append(value)
            remaining -= value
        return pattern

    else:
        return generate_rhythmic_pattern(measure_duration, rng)

def generate_rhythmic_pattern(total_beats, rng):
    """
    Generates a rhythmic pattern for a measure or phrase.
    - total_beats: total duration of the measure/phrase in beats
    - rng: random generator
    Returns a list of durations that sum to total_beats.
    """
    pattern = []
    remaining = total_beats

    while remaining > 0:
        possible = [v for v in DURATIONS.values() if v <= remaining]
        d = rng.choice(possible)
        pattern.append(d)
        remaining -= d

    return pattern