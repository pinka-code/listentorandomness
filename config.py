from dataclasses import dataclass
import tempo
import signature
from armature import Armature

@dataclass(frozen=True)
class MusicConfig:
    armature_nom: Armature
    notes_gamme: list
    tempo_nom: str
    tempo_bpm: int
    signature_nom: str
    signature_num: int
    signature_den: int
    signature_type: str
    num_pistes: int
    duree_totale: float
    longueur_phrase_min: int
    longueur_phrase_max: int
    variation_phrase_prob: float
    prob_resolution_tonique: float
    tonique_midi: int

def generer_structure(rng):
    tempo_nom, tempo_bpm = tempo.choisir_tempo_avec_nom(rng)
    armature_obj = Armature.choisir_armature(rng)
    nom_armature = armature_obj.name
    notes_gamme = armature_obj.generer_gamme()
    signature_nom, sig_num, sig_den, sig_type = signature.choisir_signature(rng)
    num_pistes = rng.randint(1, 5)
    duree_totale = rng.randint(30, 180)

    longueur_phrase_min = 1
    longueur_phrase_max = 4
    variation_phrase_prob = 0.7   # 70 % de chance de varier le motif
    prob_resolution_tonique = 0.5 # 50 % de chance de résoudre la phrase

    tonique_midi = armature_obj.tonique()

    return MusicConfig(
        armature_nom = nom_armature,
        notes_gamme = notes_gamme,
        tempo_nom=tempo_nom,
        tempo_bpm=tempo_bpm,
        signature_nom=signature_nom,
        signature_num=sig_num,
        signature_den=sig_den,
        signature_type=sig_type,
        num_pistes=num_pistes,
        duree_totale=duree_totale,
        longueur_phrase_min=longueur_phrase_min,
        longueur_phrase_max=longueur_phrase_max,
        variation_phrase_prob=variation_phrase_prob,
        prob_resolution_tonique=prob_resolution_tonique,
        tonique_midi=tonique_midi
    )
