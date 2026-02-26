from listener_to_randomness.midi.orchestration import Role
from . import octaves, rhythm

class RoleBehavior:
    """
    Responsibilities:
    - Define musical identity of a role (melody, harmony, bass, pad, etc.)
    - Control pitch selection (degree + octave)
    - Control expressive parameters (velocity shaping)
    - Define rhythmic behavior
    - Define phrase structure length
    - Provide a final resolution note behavior
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
        oct = [octaves.Octave.OCTAVE_3, octaves.Octave.OCTAVE_4]
        return octaves.choose_octave(self.rng, oct)

    def adjust_velocity(self, velocity: int, idx=0) -> int:
        """Adjust velocity based on the role (no change by default)."""
        return velocity

    def choose_pitch(self, degree: int, octave: int) -> int:
        """Returns the final MIDI pitch based on degree and octave."""
        base_note = self.config.scale_notes[degree % len(self.config.scale_notes)]
        return base_note + 12 * octave
    
    def generate_rhythm(self, measure_duration):
        return rhythm.generate_rhythmic_pattern(
            measure_duration,
            self.rng,
            rest_probability=0.0
        )
    
    def phrase_length(self):
        return 4

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
        oct = [octaves.Octave.OCTAVE_4, octaves.Octave.OCTAVE_5]
        return octaves.choose_octave(self.rng, oct)

    def adjust_velocity(self, velocity: int, idx=0) -> int:
        return min(127, velocity + 10)
    
    def generate_rhythm(self, measure_duration):
        return rhythm.generate_rhythmic_pattern(
            measure_duration,
            self.rng,
            rest_probability=0.15
        )
    
    def phrase_length(self):
        return 4

    def choose_final_note(self):
        degree = 0
        octave = self.choose_octave()
        duration_ratio = 0.5
        pitch = self.choose_pitch(degree, octave)
        return pitch, duration_ratio

class RoleHarmony(RoleBehavior):
    name = Role.HARMONY

    def choose_octave(self):
        oct = [octaves.Octave.OCTAVE_3, octaves.Octave.OCTAVE_4]
        return octaves.choose_octave(self.rng, oct)

    def adjust_velocity(self, velocity: int, idx=0) -> int:
        return velocity

    def generate_rhythm(self, measure_duration):
        return rhythm.generate_rhythmic_pattern(
            measure_duration,
            self.rng,
            rest_probability=0.05
        )
    
    def phrase_length(self):
        return 2

    def choose_final_note(self):
        degree = 0
        octave = self.choose_octave()
        duration_ratio = 1.0
        pitch = self.choose_pitch(degree, octave)
        return pitch, duration_ratio

class RoleBass(RoleBehavior):
    name = Role.BASS

    def choose_degree(self, measure=None, motif_idx=0):
        return self.rng.choice([0, 4])  # tonic or fifth

    def choose_octave(self):
        oct = [octaves.Octave.OCTAVE_1, octaves.Octave.OCTAVE_2]
        return octaves.choose_octave(self.rng, oct)

    def adjust_velocity(self, velocity: int, idx=0) -> int:
        return min(127, velocity + 5)
    
    def generate_rhythm(self, measure_duration):
        return [(1.0, False) for _ in range(int(measure_duration))]
    
    def phrase_length(self):
        return 8

    def choose_final_note(self):
        degree = 0
        octave = self.rng.choice([1, 2])
        duration_ratio = 0.5
        pitch = self.choose_pitch(degree, octave)
        return pitch, duration_ratio


class RolePad(RoleBehavior):
    name = Role.PAD

    def choose_octave(self):
        oct = [octaves.Octave.OCTAVE_3, octaves.Octave.OCTAVE_4]
        return octaves.choose_octave(self.rng, oct)

    def adjust_velocity(self, velocity: int, idx=0) -> int:
        return max(20, velocity - 10)
    
    def generate_rhythm(self, measure_duration):
        return [measure_duration]
    
    def phrase_length(self):
        return 8

    def choose_final_note(self):
        degree = 0
        octave = self.choose_octave()
        duration_ratio = 1.0
        pitch = self.choose_pitch(degree, octave)
        return pitch, duration_ratio


class RoleCountermelody(RoleBehavior):
    name = Role.COUNTERMELODY

    def choose_octave(self):
        oct = [octaves.Octave.OCTAVE_3, octaves.Octave.OCTAVE_4]
        return octaves.choose_octave(self.rng, oct)

    def adjust_velocity(self, velocity: int, idx=0) -> int:
        return min(127, velocity + 5)
    
    def generate_rhythm(self, measure_duration):
        return rhythm.generate_rhythmic_pattern(
            measure_duration,
            self.rng,
            rest_probability=0.25
        )
    
    def phrase_length(self):
        return 4

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
        Role.HARMONY: RoleHarmony,
        Role.BASS: RoleBass,
        Role.PAD: RolePad,
        Role.COUNTERMELODY: RoleCountermelody,
    }
    RoleClass = mapping.get(role_name, RoleBehavior)
    return RoleClass(config=config, rng=rng)