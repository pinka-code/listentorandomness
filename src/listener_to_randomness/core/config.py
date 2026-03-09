from dataclasses import dataclass

@dataclass(frozen=True)
class MusicConfig:
    num_tracks: int

    melodic_pattern_length_min: int
    melodic_pattern_length_max: int

    phrase_variation_prob: float

def generate_structure(rng):
    num_tracks = rng.randint(1, 5)

    melodic_pattern_length_min = 1
    melodic_pattern_length_max = 4

    phrase_variation_prob = 0.7

    return MusicConfig(
        num_tracks=num_tracks,

        melodic_pattern_length_min=melodic_pattern_length_min,
        melodic_pattern_length_max=melodic_pattern_length_max,

        phrase_variation_prob=phrase_variation_prob,
    )