from dataclasses import dataclass

@dataclass(frozen=True)
class MusicConfig:
    num_tracks: int

def generate_structure(rng):
    num_tracks = rng.randint(1, 5)

    return MusicConfig(
        num_tracks=num_tracks
    )