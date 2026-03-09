from enum import Enum
import pretty_midi


class InstrumentType(Enum):
    # Piano
    ACOUSTIC_GRAND_PIANO = ("Acoustic Grand Piano", 0)
    BRIGHT_ACOUSTIC_PIANO = ("Bright Acoustic Piano", 1)

    # Guitar
    ACOUSTIC_GUITAR_NYLON = ("Acoustic Guitar (nylon)", 24)
    ACOUSTIC_GUITAR_STEEL = ("Acoustic Guitar (steel)", 25)
    ELECTRIC_GUITAR_JAZZ = ("Electric Guitar (jazz)", 26)

    # Bass
    ACOUSTIC_BASS = ("Acoustic Bass", 32)
    ELECTRIC_BASS_FINGER = ("Electric Bass (finger)", 33)

    # Strings
    VIOLIN = ("Violin", 40)
    VIOLA = ("Viola", 41)
    CELLO = ("Cello", 42)
    CONTRABASS = ("Contrabass", 43)
    STRING_ENSEMBLE_1 = ("String Ensemble 1", 48)

    # Woodwinds
    FLUTE = ("Flute", 73)
    OBOE = ("Oboe", 68)
    CLARINET = ("Clarinet", 71)
    BASSOON = ("Bassoon", 70)
    PICCOLO = ("Piccolo", 72)

    # Brass
    TRUMPET = ("Trumpet", 56)
    TROMBONE = ("Trombone", 57)
    FRENCH_HORN = ("French Horn", 60)
    TUBA = ("Tuba", 58)

    # Organs
    CHURCH_ORGAN = ("Church Organ", 19)

    # Synths
    LEAD_SQUARE = ("Lead 1 (square)", 80)
    PAD_NEW_AGE = ("Pad 1 (new age)", 88)

    def __init__(self, label, program):
        self.label = label
        self.program = program

    def create_pretty_midi(self):
        return pretty_midi.Instrument(
            program=self.program,
            name=self.label
        )

class Instrument:
    """
    Instrument utilisé dans le moteur musical.
    """
    def __init__(self, midi, name, sound):
        self.midi = midi
        self.name = name
        self.sound = sound