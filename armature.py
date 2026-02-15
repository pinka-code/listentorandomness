from enum import Enum

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
