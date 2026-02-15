from dataclasses import dataclass

@dataclass(frozen=True)
class MusicConfig:
    gamme_nom: str
    gamme_notes: list
    tempo_nom: str
    tempo_bpm: int
    num_pistes: int
    duree_totale: float
