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

def generer_gamme(armature):
    """
    Calcule la gamme associée à l'armature.
    Retourne une liste de pitchs modulo 12.
    """
    mode = armature.mode()
    tonic = armature.tonique()

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
