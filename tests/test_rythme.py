import pytest # type: ignore
import random
import rythme

@pytest.fixture
def rng():
    return random.Random(42)

def test_choisir_duree_valeur_valide(rng):
    duree = rythme.choisir_duree(rng)
    assert duree in rythme.DUREES.values()

@pytest.mark.parametrize("probabilite", [0.0, 0.2, 0.5, 1.0])
def test_generer_silence_valeur_et_probabilite(rng, probabilite):
    essais = 1000
    resultats = [rythme.generer_silence(rng, probabilite) for _ in range(essais)]
    # toutes les valeurs doivent être bool
    assert all(isinstance(r, bool) for r in resultats)
    # On vérifie que la proportion est proche de la probabilité
    proportion = sum(resultats) / essais
    assert abs(proportion - probabilite) < 0.05  # tolérance 5%

@pytest.mark.parametrize("longueur_beats", [1.0, 2.0, 4.0])
def test_generer_motif_rythmique_somme_correcte(rng, longueur_beats):
    motif = rythme.generer_motif_rythmique(longueur_beats, rng)
    somme = sum(motif)
    assert abs(somme - longueur_beats) < 1e-6
    assert all(d in rythme.DUREES.values() for d in motif)

@pytest.mark.parametrize("role", ["pad", "basse", "harmonie", "contrechant", "melodie"])
def test_generer_motif_rythmique_pour_role_somme_correcte(rng, role):
    duree_mesure = 4.0
    motif = rythme.generer_motif_rythmique_pour_role(duree_mesure, rng, role)
    somme = sum(motif)
    assert abs(somme - duree_mesure) < 1e-6

    # Vérifications spécifiques par rôle
    if role == "pad":
        assert len(motif) == 1
        assert motif[0] == duree_mesure
    elif role == "basse":
        assert all(d == 1.0 for d in motif)
        assert len(motif) == int(duree_mesure)
    elif role == "harmonie":
        assert all(d > 0 for d in motif)
        assert somme == pytest.approx(duree_mesure, abs=1e-6)
    elif role == "melodie":
        assert all(d <= 1.0 for d in motif)
    elif role == "contrechant":
        assert all(d > 0 for d in motif)
        assert somme == pytest.approx(duree_mesure, abs=1e-6)
