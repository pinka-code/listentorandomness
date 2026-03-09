from enum import Enum
from listener_to_randomness.midi.note import Note

class WaveType(Enum):
    SINE = "sine"
    SQUARE = "square"
    SAW = "saw"
    TRIANGLE = "triangle"

class ADSR:
    """
    Attack-Decay-Sustain-Release envelope
    All values are fractions of note duration for attack/decay/release,
    and sustain is a multiplier for velocity
    """
    def __init__(self, attack: float, decay: float, sustain: float, release: float):
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release

class SoundDesign:
    WAVE_TYPES = [WaveType.SINE, WaveType.SQUARE, WaveType.SAW, WaveType.TRIANGLE]

    def __init__(self, rng):
        self.rng = rng
        self.wave = rng.choice(self.WAVE_TYPES)

        # ADSR randomly chosen
        self.adsr = ADSR(
            attack=rng.choice([0.01, 0.05, 0.1]),
            decay=rng.choice([0.05, 0.1, 0.2]),
            sustain=rng.choice([0.6, 0.7, 0.8, 1.0]),
            release=rng.choice([0.05, 0.1, 0.2])
        )

    def apply(self, pitch: int, start: float, duration: float, velocity: int):
        """
        Apply sound design to a single note.
        Modifies:
          - velocity based on sustain
          - duration shortened by release fraction
        """
        adjusted_velocity = int(velocity * self.adsr.sustain)
        final_duration = duration * (1.0 - self.adsr.release * 0.5)

        if self.wave == WaveType.SAW:
            adjusted_velocity = min(127, int(adjusted_velocity * 1.05))
        elif self.wave == WaveType.SQUARE:
            adjusted_velocity = min(127, int(adjusted_velocity * 1.1))
        elif self.wave == WaveType.TRIANGLE:
            adjusted_velocity = int(adjusted_velocity * 0.9)
        # SINE is neutral

        return [Note(pitch, start, final_duration, adjusted_velocity)]
