from dataclasses import dataclass

from .time_signature import TimeSignature
from .key_signature import KeySignature


@dataclass(frozen=True)
class MusicConfig:
    key_name: str
    scale_notes: list

    time_signature_name: str
    time_signature_num: int
    time_signature_den: int

    num_tracks: int

    pattern_length_min: int
    pattern_length_max: int

    phrase_variation_prob: float

    tonic_midi: int

    def measure_duration_quarters(self) -> float:
        """
        Duration of one measure in quarter-note units.
        (1.0 = quarter note)
        """
        return self.time_signature_num * (4 / self.time_signature_den)

def generate_structure(rng):
    key_obj = KeySignature.choose(rng)
    key_name = key_obj.name
    scale_notes = key_obj.generate_scale()

    time_signature = TimeSignature.choose(rng)

    num_tracks = rng.randint(1, 5)

    pattern_length_min = 1
    pattern_length_max = 4

    phrase_variation_prob = 0.7

    tonic_midi = key_obj.tonic()

    return MusicConfig(
        key_name=key_name,
        scale_notes=scale_notes,

        time_signature_name=time_signature.name,
        time_signature_num=time_signature.numerator,
        time_signature_den=time_signature.denominator,

        num_tracks=num_tracks,

        pattern_length_min=pattern_length_min,
        pattern_length_max=pattern_length_max,

        phrase_variation_prob=phrase_variation_prob,

        tonic_midi=tonic_midi,
    )