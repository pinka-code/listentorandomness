from dataclasses import dataclass



@dataclass(frozen=True)
class MusicConfig:
    orchestration_density: int

    DENSITY_MAP = {
        "sparse": 0.4,
        "normal": 0.7,
        "dense": 1.0,
    }

    @property
    def density_factor(self):
        return self.DENSITY_MAP[self.orchestration_density]

def generate_structure(rng):
    orchestration_density = rng.choice(["sparse", "normal", "dense"])

    return MusicConfig(
        orchestration_density=orchestration_density
    )