import pretty_midi # type: ignore
from random import Random
from mesure import Mesure

class FakeRole:
    nom = "fake"

    def choisir_degre(self, mesure, motif_idx):
        # retourne simplement le degré du motif
        return mesure.motif[motif_idx % len(mesure.motif)]

    def choisir_octave(self, mesure):
        # octave fixe pour tests
        return 4

    def ajuster_velocity(self, velocity):
        return velocity

    def choisir_note_finale(self, mesure, config, rng):
        # tonique fixe, octave fixe, demi-mesure
        return 0, 4, 0.5

class FakeConfig:
    def __init__(self):
        self.notes_gamme = [60, 62, 64, 65, 67, 69, 71]  # Do majeur
        self.signature_num = 4
        self.signature_den = 4


def test_mesure_avance_le_temps():
    rng = Random(42)
    config = FakeConfig()
    motif = [0, 2, 4]
    motif_rythmique = [1, 1, 1, 1]
    role = FakeRole()
    instr = pretty_midi.Instrument(program=0)
    
    m = Mesure(motif, motif_rythmique, role, "Piano", config, rng)
    time_depart = 0.0
    time_fin = m.jouer(instr, time_depart, nuance_phrase=64)
    
    assert time_fin > time_depart, "La mesure doit avancer le temps"

def test_mesure_joue_le_bon_nombre_de_notes():
    rng = Random(42)
    config = FakeConfig()
    motif = [0, 2, 4]
    motif_rythmique = [0.5, 0.5, 0.5, 0.5]
    role = FakeRole()
    instr = pretty_midi.Instrument(program=0)
    
    m = Mesure(motif, motif_rythmique, role, "Piano", config, rng)
    m._est_silence = lambda: False  # désactiver les silences aléatoires pour ce test
    m.jouer(instr, 0.0, nuance_phrase=64)
    
    assert len(instr.notes) == len(motif_rythmique), "Doit créer une note par durée du motif rythmique"

def test_mesure_transmet_la_nuance():
    rng = Random(42)
    config = FakeConfig()
    motif = [0, 2, 4]
    motif_rythmique = [1, 1, 1]
    role = FakeRole()
    instr = pretty_midi.Instrument(program=0)
    
    nuance_phrase = 70
    m = Mesure(motif, motif_rythmique, role, "Piano", config, rng)
    m.jouer(instr, 0.0, nuance_phrase=nuance_phrase)
    
    for note in instr.notes:
        assert note.velocity >= nuance_phrase, "Chaque note doit avoir au moins la vélocité de la phrase"

def test_ajouter_tonique_ajoute_une_note():
    rng = Random(42)
    config = FakeConfig()
    motif = [0, 2, 4]
    motif_rythmique = [1, 1, 1]
    role = FakeRole()
    instr = pretty_midi.Instrument(program=0)
    
    m = Mesure(motif, motif_rythmique, role, "Piano", config, rng)
    time_depart = 0.0
    time_fin = m.ajouter_tonique(instr, time_depart, nuance_phrase=64)
    
    assert len(instr.notes) == 1
    assert instr.notes[0].pitch == config.notes_gamme[0] + 12*4, "Tonique doit être la première note de la gamme + octave"
    assert time_fin > time_depart

def test_mesure_est_deterministe_avec_seed():
    seed = 12345
    motif = [0, 2, 4]
    motif_rythmique = [1, 1, 1, 1]
    config = FakeConfig()
    role = FakeRole()
    
    instr1 = pretty_midi.Instrument(program=0)
    instr2 = pretty_midi.Instrument(program=0)
    
    m1 = Mesure(motif, motif_rythmique, role, "Piano", config, Random(seed))
    m2 = Mesure(motif, motif_rythmique, role, "Piano", config, Random(seed))
    
    m1.jouer(instr1, 0.0, nuance_phrase=64)
    m2.jouer(instr2, 0.0, nuance_phrase=64)
    
    pitches1 = [n.pitch for n in instr1.notes]
    pitches2 = [n.pitch for n in instr2.notes]
    
    assert pitches1 == pitches2, "Deux exécutions avec même seed doivent produire le même résultat"
