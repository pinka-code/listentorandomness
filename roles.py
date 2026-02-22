from orchestration import Role

class RoleBehavior:
    """
    Responsibilities:
    - Determine the pitch from a musical degree
    - Adjust velocity according to musical context
    - Provide the final resolution note
    - Encapsulate specific musical behavior for a role (melody, bass, accompaniment, etc.)
    """

    name = "default"

    def __init__(self, config, rng=None):
        self.config = config
        self.rng = rng

    def choose_degree(self, measure=None, motif_idx=0):
        """Chooses the degree in the pattern (default: cyclic)."""
        if measure:
            return measure.motif[motif_idx % len(measure.motif)]
        return 0

    def choose_octave(self):
        """Default octave (3 or 4)."""
        return self.rng.choice([3, 4])

    def adjust_velocity(self, velocity: int, idx=0) -> int:
        """Adjust velocity based on the role (no change by default)."""
        return velocity

    def choose_pitch(self, degree: int, octave: int) -> int:
        """Returns the final MIDI pitch based on degree and octave."""
        base_note = self.config.scale_notes[degree % len(self.config.scale_notes)]
        return base_note + 12 * octave

    def choose_final_note(self):
        """Returns a tuple (pitch, duration_ratio) for the final note."""
        degree = 0
        octave = self.choose_octave()
        duration_ratio = 0.5
        pitch = self.choose_pitch(degree, octave)
        return pitch, duration_ratio


class RoleMelody(RoleBehavior):
    name = Role.MELODY

    def choose_octave(self):
        return self.rng.choice([4, 5])

    def adjust_velocity(self, velocity: int, idx=0) -> int:
        return min(127, velocity + 10)

    def choose_final_note(self):
        degree = 0
        octave = self.choose_octave()
        duration_ratio = 0.5
        pitch = self.choose_pitch(degree, octave)
        return pitch, duration_ratio


class RoleBass(RoleBehavior):
    name = Role.BASS

    def choose_degree(self, measure=None, motif_idx=0):
        return self.rng.choice([0, 4])  # tonic or fifth

    def choose_octave(self):
        return self.rng.choice([1, 2])

    def adjust_velocity(self, velocity: int, idx=0) -> int:
        return min(127, velocity + 5)

    def choose_final_note(self):
        degree = 0
        octave = self.rng.choice([1, 2])
        duration_ratio = 0.5
        pitch = self.choose_pitch(degree, octave)
        return pitch, duration_ratio


class RolePad(RoleBehavior):
    name = Role.PAD

    def choose_octave(self):
        return self.rng.choice([3, 4])

    def adjust_velocity(self, velocity: int, idx=0) -> int:
        return max(20, velocity - 10)

    def choose_final_note(self):
        degree = 0
        octave = self.choose_octave()
        duration_ratio = 1.0
        pitch = self.choose_pitch(degree, octave)
        return pitch, duration_ratio


class RoleCountermelody(RoleBehavior):
    name = Role.COUNTERMELODY

    def choose_octave(self):
        return self.rng.choice([3, 4])

    def adjust_velocity(self, velocity: int, idx=0) -> int:
        return min(127, velocity + 5)

    def choose_final_note(self):
        degree = 0
        octave = self.choose_octave()
        duration_ratio = 0.5
        pitch = self.choose_pitch(degree, octave)
        return pitch, duration_ratio


def create_role(role_name: str, config=None, rng=None) -> RoleBehavior:
    """Returns the role object corresponding to the name and instantiates it."""
    mapping = {
        Role.MELODY: RoleMelody,
        Role.BASS: RoleBass,
        Role.PAD: RolePad,
        Role.COUNTERMELODY: RoleCountermelody,
    }
    RoleClass = mapping.get(role_name, RoleBehavior)
    return RoleClass(config=config, rng=rng)