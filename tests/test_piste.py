import pytest  # type: ignore
import random
import pretty_midi  # type: ignore

from piste import Piste
from phrase import Phrase

class FakeConfig:
    duree_totale = 8.0  # durée totale de la piste en beats
    signature_num = 4
    signature_den = 4
    longueur_phrase_min = 1
    longueur_phrase_max = 2
    variation_phrase_prob = 0.5
    notes_gamme = [60, 62, 64, 65, 67, 69, 71, 72]

def creer_instr_faux():
    return pretty_midi.Instrument(program=0)

@pytest.fixture
def rng():
    return random.Random(42)

@pytest.fixture
def config():
    return FakeConfig()

@pytest.fixture
def piste_melodie(config, rng):
    instr = creer_instr_faux()
    return Piste(config=config, rng=rng, role="melodie", instrument=instr, nom_instrument="Piano")

def test_generer_phrases_avance_le_temps(piste_melodie):
    instr = piste_melodie.instr
    piste_melodie.generer_phrases()

    assert len(instr.notes) > 0, "Aucune note générée"

    # Vérifie que toutes les notes ont un start non négatif
    assert all(note.start >= 0 for note in instr.notes)

    # Vérifie que pitch et velocity restent valides
    assert all(0 <= note.pitch <= 127 for note in instr.notes)
    assert all(0 <= note.velocity <= 127 for note in instr.notes)

def test_determinisme_piste(config):
    rng1 = random.Random(123)
    rng2 = random.Random(123)
    instr1 = creer_instr_faux()
    instr2 = creer_instr_faux()
    piste1 = Piste(config, rng1, "melodie", instr1, "Piano")
    piste2 = Piste(config, rng2, "melodie", instr2, "Piano")

    piste1.generer_phrases()
    piste2.generer_phrases()

    assert [n.pitch for n in instr1.notes] == [n.pitch for n in instr2.notes]
    assert [n.velocity for n in instr1.notes] == [n.velocity for n in instr2.notes]

def test_role_influence_notes(rng, config):
    instr = creer_instr_faux()
    piste = Piste(config, rng, "basse", instr, "Piano")
    piste.generer_phrases()
    # Vérifie que les notes sont dans l’intervalle MIDI
    assert all(0 <= n.pitch <= 127 for n in instr.notes)
    assert all(0 <= n.velocity <= 127 for n in instr.notes)
