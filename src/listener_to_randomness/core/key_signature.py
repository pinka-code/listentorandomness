from enum import Enum

INTERVALS = {
    "major": [2, 2, 1, 2, 2, 2, 1],
    "minor": [2, 1, 2, 2, 1, 2, 2]
}

NOTE_TO_MIDI = {
    "C": 0,
    "C#": 1, "Db": 1,
    "D": 2,
    "D#": 3, "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6, "Gb": 6,
    "G": 7,
    "G#": 8, "Ab": 8,
    "A": 9,
    "A#": 10, "Bb": 10,
    "B": 11
}

class KeySignature(Enum):
    # Major keys
    C_MAJOR = ("C", "major", 0)
    G_MAJOR = ("G", "major", 1)
    D_MAJOR = ("D", "major", 2)
    A_MAJOR = ("A", "major", 3)
    E_MAJOR = ("E", "major", 4)
    B_MAJOR = ("B", "major", 5)
    F_MAJOR = ("F", "major", -1)
    BB_MAJOR = ("Bb", "major", -2)
    EB_MAJOR = ("Eb", "major", -3)
    AB_MAJOR = ("Ab", "major", -4)

    # Minor keys
    A_MINOR = ("A", "minor", 0)
    E_MINOR = ("E", "minor", 1)
    B_MINOR = ("B", "minor", 2)
    F_SHARP_MINOR = ("F#", "minor", 3)
    C_SHARP_MINOR = ("C#", "minor", 4)
    D_MINOR = ("D", "minor", -1)
    G_MINOR = ("G", "minor", -2)
    C_MINOR = ("C", "minor", -3)
    F_MINOR = ("F", "minor", -4)
    BB_MINOR = ("Bb", "minor", -2)
    EB_MINOR = ("Eb", "minor", -3)
    G_SHARP_MINOR = ("G#", "minor", 5)

    def tonic(self):
        return self.value[0]

    def mode(self):
        return self.value[1]

    @staticmethod
    def choose(rng):
        """Randomly choose a key signature"""
        return rng.choice(list(KeySignature))

    def generate_scale(self):
        """Compute the scale notes modulo 12"""
        mode = self.mode()
        tonic = self.tonic()
        if mode not in INTERVALS:
            raise ValueError(f"Unknown mode: {mode}")
        intervals = INTERVALS[mode]
        base = NOTE_TO_MIDI[tonic]
        notes = [base % 12]
        value = base
        for interval in intervals[:-1]:
            value += interval
            notes.append(value % 12)
        return notes

    def choose_neighbour_key(self, rng, same_prob=0.7):
        """Choose a neighbor key with probability to stay on the same key"""
        if rng.random() < same_prob:
            return self
        neighbor_keys = NEIGHBOR_KEYS.get(self, [])
        if not neighbor_keys:
            return self
        return rng.choice(neighbor_keys)


NEIGHBOR_KEYS = {
    # Major keys
    KeySignature.C_MAJOR: [KeySignature.G_MAJOR, KeySignature.F_MAJOR, KeySignature.A_MINOR, KeySignature.C_MINOR],
    KeySignature.G_MAJOR: [KeySignature.D_MAJOR, KeySignature.C_MAJOR, KeySignature.E_MINOR, KeySignature.G_MINOR],
    KeySignature.D_MAJOR: [KeySignature.A_MAJOR, KeySignature.G_MAJOR, KeySignature.B_MINOR, KeySignature.D_MINOR],
    KeySignature.A_MAJOR: [KeySignature.E_MAJOR, KeySignature.D_MAJOR, KeySignature.F_SHARP_MINOR, KeySignature.A_MINOR],
    KeySignature.E_MAJOR: [KeySignature.B_MAJOR, KeySignature.A_MAJOR, KeySignature.C_SHARP_MINOR, KeySignature.E_MINOR],
    KeySignature.B_MAJOR: [],  # can fill as needed
    KeySignature.F_MAJOR: [KeySignature.C_MAJOR, KeySignature.BB_MAJOR, KeySignature.D_MINOR, KeySignature.F_MINOR],
    KeySignature.BB_MAJOR: [KeySignature.F_MAJOR, KeySignature.EB_MAJOR, KeySignature.G_MINOR, KeySignature.BB_MINOR],
    KeySignature.EB_MAJOR: [KeySignature.BB_MAJOR, KeySignature.AB_MAJOR, KeySignature.C_MINOR, KeySignature.EB_MINOR],
    KeySignature.AB_MAJOR: [KeySignature.EB_MAJOR, KeySignature.F_MINOR, KeySignature.AB_MAJOR],  # simplified

    # Minor keys
    KeySignature.A_MINOR: [KeySignature.C_MAJOR, KeySignature.E_MINOR, KeySignature.D_MINOR, KeySignature.A_MAJOR],
    KeySignature.E_MINOR: [KeySignature.G_MAJOR, KeySignature.B_MINOR, KeySignature.A_MINOR, KeySignature.E_MAJOR],
    KeySignature.B_MINOR: [KeySignature.D_MAJOR, KeySignature.F_SHARP_MINOR, KeySignature.G_MINOR, KeySignature.B_MAJOR],
    KeySignature.F_SHARP_MINOR: [KeySignature.A_MAJOR, KeySignature.C_SHARP_MINOR, KeySignature.D_MINOR, KeySignature.F_SHARP_MINOR],
    KeySignature.C_SHARP_MINOR: [KeySignature.E_MAJOR, KeySignature.G_SHARP_MINOR, KeySignature.F_SHARP_MINOR, KeySignature.C_SHARP_MINOR],
    KeySignature.D_MINOR: [KeySignature.F_MAJOR, KeySignature.A_MINOR, KeySignature.G_MINOR, KeySignature.D_MAJOR],
    KeySignature.G_MINOR: [KeySignature.BB_MAJOR, KeySignature.D_MINOR, KeySignature.C_MINOR, KeySignature.G_MAJOR],
    KeySignature.C_MINOR: [KeySignature.EB_MAJOR, KeySignature.G_MINOR, KeySignature.F_MINOR, KeySignature.C_MAJOR],
    KeySignature.F_MINOR: [KeySignature.AB_MAJOR, KeySignature.C_MINOR, KeySignature.BB_MINOR, KeySignature.F_MAJOR]
}