from dataclasses import dataclass
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
