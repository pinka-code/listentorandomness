from enum import Enum

INTERVALLES = {
    "majeur": [2, 2, 1, 2, 2, 2, 1],
    "mineur": [2, 1, 2, 2, 1, 2, 2]
}

# Notes MIDI modulo 12 (Do=0, Do#=1, ...)
NOTE_TO_MIDI = {
    "C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4,
    "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9,
    "A#": 10, "B": 11
}

class Armature(Enum):
    C_MAJOR = ("C", "majeur", 0)
    G_MAJOR = ("G", "majeur", 1)
    D_MAJOR = ("D", "majeur", 2)
    A_MAJOR = ("A", "majeur", 3)
    E_MAJOR = ("E", "majeur", 4)
    B_MAJOR = ("B", "majeur", 5)
    F_MAJOR = ("F", "majeur", -1)
    BB_MAJOR = ("Bb", "majeur", -2)
    EB_MAJOR = ("Eb", "majeur", -3)
    AB_MAJOR = ("Ab", "majeur", -4)

    A_MINOR = ("A", "mineur", 0)
    E_MINOR = ("E", "mineur", 1)
    B_MINOR = ("B", "mineur", 2)
    F_SHARP_MINOR = ("F#", "mineur", 3)
    C_SHARP_MINOR = ("C#", "mineur", 4)
    D_MINOR = ("D", "mineur", -1)
    G_MINOR = ("G", "mineur", -2)
    C_MINOR = ("C", "mineur", -3)
    F_MINOR = ("F", "mineur", -4)

    def tonique(self):
        return self.value[0]

    def mode(self):
        return self.value[1]

    @staticmethod
    def choisir_armature(rng):
        return rng.choice(list(Armature))
    
    def generer_gamme(self):
        """
        Calcule la gamme associée à l'armature.
        Retourne une liste de pitchs modulo 12.
        """
        mode = self.mode()
        tonic = self.tonique()

        if mode not in INTERVALLES:
            raise ValueError(f"Mode inconnu : {mode}")

        intervalles = INTERVALLES[mode]
        base = NOTE_TO_MIDI[tonic]

        notes = [base % 12]
        valeur = base
        for intervalle in intervalles[:-1]:
            valeur += intervalle
            notes.append(valeur % 12)
        return notes

