from enum import Enum
from listener_to_randomness.midi.note import Note


class ArticulationType(Enum):
    NORMAL = "normal"
    STACCATO = "staccato"
    LEGATO = "legato"
    TRILL = "trill"


class Articulation:

    TYPES = [
        ArticulationType.NORMAL,
        ArticulationType.STACCATO,
        ArticulationType.LEGATO,
        ArticulationType.TRILL,
    ]

    WEIGHTS = [
        6,  # normal (majorité)
        2,  # staccato
        1,  # legato
        1,  # trill
    ]

    def __init__(self, rng):
        self.rng = rng
        self.type = rng.choice_weighted(self.TYPES, self.WEIGHTS)

    def apply(self, pitch, start, duration, velocity):

        if self.type == ArticulationType.STACCATO:
            return [Note(pitch, start, duration * 0.5, velocity)]

        if self.type == ArticulationType.LEGATO:
            return [Note(pitch, start, duration * 0.95, velocity)]

        if self.type == ArticulationType.TRILL:
            step = duration / 4
            return [
                Note(pitch, start, step, velocity),
                Note(pitch + 1, start + step, step, velocity),
                Note(pitch, start + 2 * step, step, velocity),
                Note(pitch + 1, start + 3 * step, step, velocity),
            ]

        return [Note(pitch, start, duration, velocity)]