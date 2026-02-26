from enum import Enum

INTERVALS = {
    "major": [2, 2, 1, 2, 2, 2, 1],
    "minor": [2, 1, 2, 2, 1, 2, 2]
}

# MIDI notes modulo 12 (C=0, C#=1, ...)
NOTE_TO_MIDI = {
    "C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4,
    "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9,
    "A#": 10, "B": 11
}

class KeySignature(Enum):
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

    A_MINOR = ("A", "minor", 0)
    E_MINOR = ("E", "minor", 1)
    B_MINOR = ("B", "minor", 2)
    F_SHARP_MINOR = ("F#", "minor", 3)
    C_SHARP_MINOR = ("C#", "minor", 4)
    D_MINOR = ("D", "minor", -1)
    G_MINOR = ("G", "minor", -2)
    C_MINOR = ("C", "minor", -3)
    F_MINOR = ("F", "minor", -4)

    def tonic(self):
        return self.value[0]

    def mode(self):
        return self.value[1]

    @staticmethod
    def choose_key_signature(rng):
        return rng.choice(list(KeySignature))
    
    def generate_scale(self):
        """
        Computes the scale associated with the key signature.
        Returns a list of pitches modulo 12.
        """
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