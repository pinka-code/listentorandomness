# gammes.py
import random

NOTE = {
    "C": 0,
    "C#": 1,
    "D": 2,
    "D#": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "G": 7,
    "G#": 8,
    "A": 9,
    "A#": 10,
    "B": 11
}

GAMMES = {
    # Gammes majeures
    "C_major": [NOTE["C"], NOTE["D"], NOTE["E"], NOTE["F"], NOTE["G"], NOTE["A"], NOTE["B"]],
    "C#_major": [NOTE["C#"], NOTE["D#"], NOTE["F"], NOTE["F#"], NOTE["G#"], NOTE["A#"], NOTE["C"]],
    "D_major": [NOTE["D"], NOTE["E"], NOTE["F#"], NOTE["G"], NOTE["A"], NOTE["B"], NOTE["C#"]],
    "D#_major": [NOTE["D#"], NOTE["F"], NOTE["G"], NOTE["G#"], NOTE["A#"], NOTE["C"], NOTE["D"]],
    "E_major": [NOTE["E"], NOTE["F#"], NOTE["G#"], NOTE["A"], NOTE["B"], NOTE["C#"], NOTE["D#"]],
    "F_major": [NOTE["F"], NOTE["G"], NOTE["A"], NOTE["A#"], NOTE["C"], NOTE["D"], NOTE["E"]],
    "F#_major": [NOTE["F#"], NOTE["G#"], NOTE["A#"], NOTE["B"], NOTE["C#"], NOTE["D#"], NOTE["F"]],
    "G_major": [NOTE["G"], NOTE["A"], NOTE["B"], NOTE["C"], NOTE["D"], NOTE["E"], NOTE["F#"]],
    "G#_major": [NOTE["G#"], NOTE["A#"], NOTE["C"], NOTE["C#"], NOTE["D#"], NOTE["F"], NOTE["G"]],
    "A_major": [NOTE["A"], NOTE["B"], NOTE["C#"], NOTE["D"], NOTE["E"], NOTE["F#"], NOTE["G#"]],
    "A#_major": [NOTE["A#"], NOTE["C"], NOTE["D"], NOTE["D#"], NOTE["F"], NOTE["G"], NOTE["A"]],
    "B_major": [NOTE["B"], NOTE["C#"], NOTE["D#"], NOTE["E"], NOTE["F#"], NOTE["G#"], NOTE["A#"]],

    # Gammes mineures naturelles
    "C_minor": [NOTE["C"], NOTE["D"], NOTE["D#"], NOTE["F"], NOTE["G"], NOTE["G#"], NOTE["A#"]],
    "C#_minor": [NOTE["C#"], NOTE["D#"], NOTE["E"], NOTE["F#"], NOTE["G#"], NOTE["A"], NOTE["B"]],
    "D_minor": [NOTE["D"], NOTE["E"], NOTE["F"], NOTE["G"], NOTE["A"], NOTE["A#"], NOTE["C"]],
    "D#_minor": [NOTE["D#"], NOTE["F"], NOTE["F#"], NOTE["G#"], NOTE["A#"], NOTE["B"], NOTE["C#"]],
    "E_minor": [NOTE["E"], NOTE["F#"], NOTE["G"], NOTE["A"], NOTE["B"], NOTE["C"], NOTE["D"]],
    "F_minor": [NOTE["F"], NOTE["G"], NOTE["G#"], NOTE["A#"], NOTE["C"], NOTE["C#"], NOTE["D#"]],
    "F#_minor": [NOTE["F#"], NOTE["G#"], NOTE["A"], NOTE["B"], NOTE["C#"], NOTE["D"], NOTE["E"]],
    "G_minor": [NOTE["G"], NOTE["A"], NOTE["A#"], NOTE["C"], NOTE["D"], NOTE["D#"], NOTE["F"]],
    "G#_minor": [NOTE["G#"], NOTE["A#"], NOTE["B"], NOTE["C#"], NOTE["D#"], NOTE["E"], NOTE["F#"]],
    "A_minor": [NOTE["A"], NOTE["B"], NOTE["C"], NOTE["D"], NOTE["E"], NOTE["F"], NOTE["G"]],
    "A#_minor": [NOTE["A#"], NOTE["C"], NOTE["C#"], NOTE["D#"], NOTE["F"], NOTE["F#"], NOTE["G#"]],
    "B_minor": [NOTE["B"], NOTE["C#"], NOTE["D"], NOTE["E"], NOTE["F#"], NOTE["G"], NOTE["A"]]
}

def choisir_gamme():
    """Retourne (nom_gamme, notes_gamme)"""
    return random.choice(list(GAMMES.items()))

def choisir_note(gamme_notes):
    """Retourne une note de la gamme"""
    return random.choice(gamme_notes)
