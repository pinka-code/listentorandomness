from dataclasses import dataclass

@dataclass(frozen=True)
class MusicConfig:
    gamme_nom: str
    gamme_notes: list
    tempo_nom: str
    tempo_bpm: int
    signature_nom: str
    signature_num: int
    signature_den: int
    signature_type: str
    num_pistes: int
    duree_totale: float
