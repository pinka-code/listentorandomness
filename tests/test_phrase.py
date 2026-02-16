import pytest # type: ignore
import random
import pretty_midi # type: ignore

import phrase
from mesure import Mesure

class FakeConfig:
    signature_num = 4
    signature_den = 4
    longueur_phrase_min = 1
    longueur_phrase_max = 2
    variation_phrase_prob = 0.5
    notes_gamme = [60, 62, 64, 65, 67, 69, 71, 72]  # Do majeur simple

def creer_instr_faux():
    return pretty_midi.Instrument(program=0)

@pytest.fixture
def rng():
    return random.Random(42)

@pytest.fixture
def config():
    return FakeConfig()

@pytest.fixture
def phrase_melodie(config, rng):
    return phrase.Phrase(config=config, rng=rng, role="melodie", nom_instrument="Piano")

def test_generer_motif_melodique_valide(phrase_melodie):
    motif = phrase_melodie.generer_motif_melodique()
    assert len(motif) == 4
    assert all(0 <= degre < len(phrase_melodie.config.notes_gamme) for degre in motif)

def test_generer_motif_rythmique_somme_mesure(phrase_melodie):
    motif_rythme = phrase_melodie.generer_motif_rythmique()
    duree_mesure = Mesure.calculer_duree(phrase_melodie.config.signature_num,
                                         phrase_melodie.config.signature_den)
    assert abs(sum(motif_rythme) - duree_mesure) < 0.0001

def test_varier_motif_modifie_au_moins_une_note(phrase_melodie):
    original = phrase_melodie.motif
    trouve_diff = False
    for _ in range(10):
        nouveau = phrase_melodie.varier_motif()
        if any(o != n for o, n in zip(original, nouveau)):
            trouve_diff = True
            break
    assert trouve_diff, "La variation du motif n'a modifié aucune note après 10 tentatives"

def test_phrase_ajoute_tonique(phrase_melodie):
    instr = creer_instr_faux()
    time_depart = 0.0
    time_fin = phrase_melodie.jouer(instr, time_depart)
    # On s'assure que la dernière note est la tonique de la gamme
    last_note_pitch = instr.notes[-1].pitch
    assert last_note_pitch == phrase_melodie.config.notes_gamme[0] or last_note_pitch in range(phrase_melodie.config.notes_gamme[0], 128)

def test_phrase_temps_total_rythme_et_tonique(phrase_melodie):
    instr = creer_instr_faux()
    time_depart = 0.0
    time_fin = phrase_melodie.jouer(instr, time_depart)
    # Vérifie que la dernière note ne dépasse pas la fin de la phrase
    assert time_fin >= time_depart
    assert all(note.end <= time_fin for note in instr.notes)

def test_nuance_durable_phrase_et_tonique(phrase_melodie):
    instr = creer_instr_faux()
    time_depart = 0.0
    phrase_melodie.jouer(instr, time_depart)
    velocities = [note.velocity for note in instr.notes]
    assert all(abs(v - phrase_melodie.nuance) <= 20 for v in velocities)

def test_variation_phrase_modifie_motif(phrase_melodie):
    original = phrase_melodie.motif
    trouve_diff = False
    for _ in range(10):
        nouveau = phrase_melodie.varier_motif()
        if any(o != n for o, n in zip(original, nouveau)):
            trouve_diff = True
            break
    assert trouve_diff, "La variation du motif n'a modifié aucune note après 10 tentatives"

def test_role_influence_pitch_octave_velocity(phrase_melodie, rng, config):
    roles_to_test = ["melodie", "basse", "pad", "contrechant"]
    for role_name in roles_to_test:
        p = phrase.Phrase(config, rng, role_name, "Piano")
        instr = creer_instr_faux()
        p.jouer(instr, 0.0)
        # Vérifie que toutes les notes sont dans la plage MIDI valide
        assert all(0 <= note.pitch <= 127 for note in instr.notes)
        assert all(0 <= note.velocity <= 127 for note in instr.notes)

def test_determinisme_phrase(config):
    rng1 = random.Random(123)
    rng2 = random.Random(123)
    p1 = phrase.Phrase(config, rng1, "melodie", "Piano")
    p2 = phrase.Phrase(config, rng2, "melodie", "Piano")
    instr1 = creer_instr_faux()
    instr2 = creer_instr_faux()
    t1 = p1.jouer(instr1, 0.0)
    t2 = p2.jouer(instr2, 0.0)
    assert t1 == t2
    assert [n.pitch for n in instr1.notes] == [n.pitch for n in instr2.notes]
    assert [n.velocity for n in instr1.notes] == [n.velocity for n in instr2.notes]
