from dataclasses import dataclass

from . import tempo
from . import time_signature
from .key_signature import KeySignature


@dataclass(frozen=True)
class MusicConfig:
    key_name: str
    scale_notes: list

    tempo_name: str
    tempo_bpm: int

    time_signature_name: str
    time_signature_num: int
    time_signature_den: int
    time_signature_type: str

    num_tracks: int
    total_duration: float

    pattern_length_min: int
    pattern_length_max: int

    phrase_variation_prob: float

    tonic_midi: int

    def beat_duration(self) -> float:
        """
        Duration of one beat in seconds.
        """
        return 60.0 / self.tempo_bpm

    def bar_duration(self) -> float:
        """
        Duration of one measure (bar) in seconds.
        """
        return self.time_signature_num * self.beat_duration()

    def total_bars(self) -> int:
        """
        Total number of bars in the composition.
        """
        return int(self.total_duration / self.bar_duration())

def generate_structure(rng):
    tempo_name, tempo_bpm = tempo.choose_tempo_with_name(rng)

    key_obj = KeySignature.choose_key_signature(rng)
    key_name = key_obj.name
    scale_notes = key_obj.generate_scale()

    (
        time_signature_name,
        sig_num,
        sig_den,
        sig_type
    ) = time_signature.choose_time_signature(rng)

    num_tracks = rng.randint(1, 5)

    total_duration = rng.randint(30, 180)

    pattern_length_min = 1
    pattern_length_max = 4

    phrase_variation_prob = 0.7

    tonic_midi = key_obj.tonic()

    return MusicConfig(
        key_name=key_name,
        scale_notes=scale_notes,

        tempo_name=tempo_name,
        tempo_bpm=tempo_bpm,

        time_signature_name=time_signature_name,
        time_signature_num=sig_num,
        time_signature_den=sig_den,
        time_signature_type=sig_type,

        num_tracks=num_tracks,
        total_duration=total_duration,

        pattern_length_min=pattern_length_min,
        pattern_length_max=pattern_length_max,

        phrase_variation_prob=phrase_variation_prob,

        tonic_midi=tonic_midi,
    )