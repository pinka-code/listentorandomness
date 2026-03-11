from listener_to_randomness.midi.orchestration import Role
from . import octaves
from .rhythm import RhythmicPattern

class RoleBehavior:
    """
    Responsibilities:
    - Define musical identity of a role (melody, harmony, bass, pad, etc.)
    - Controls pitch, octave, dynamics, rhythm, phrase length.
    """

    name = "default"

    def __init__(self, config, rng):
        self.config = config
        self.rng = rng

    def choose_octave(self):
        """Default octave (3 or 4)."""
        oct = [octaves.Octave.OCTAVE_3, octaves.Octave.OCTAVE_4]
        return octaves.choose_octave(self.rng, oct)

    def adjust_velocity(self, velocity: int) -> int:
        """Adjust velocity based on the role (no change by default)."""
        return min(127, velocity)

    def choose_pitch(self, scale_notes, degree: int) -> int:
        """Returns the final MIDI pitch based on degree and octave."""
        base_note = scale_notes[degree % len(scale_notes)]
        octave = self.choose_octave()
        return base_note + 12 * octave
    
    def generate_rhythm(self, context):
        return RhythmicPattern.generate(context)
    
    def phrase_length(self):
        return 4


class RoleMelody(RoleBehavior):
    name = Role.MELODY

    def choose_octave(self):
        oct = [octaves.Octave.OCTAVE_4, octaves.Octave.OCTAVE_5]
        return octaves.choose_octave(self.rng, oct)

    def adjust_velocity(self, velocity: int) -> int:
        return min(127, velocity + 10)
    
    def generate_rhythm(self, context):
        return RhythmicPattern.generate(context)
    
    def phrase_length(self):
        return 4

class RoleHarmony(RoleBehavior):
    name = Role.HARMONY

    def choose_octave(self):
        oct = [octaves.Octave.OCTAVE_3, octaves.Octave.OCTAVE_4]
        return octaves.choose_octave(self.rng, oct)

    def adjust_velocity(self, velocity: int) -> int:
        return min(127, velocity)

    def generate_rhythm(self, context):
        return RhythmicPattern.generate(context)
    
    def phrase_length(self):
        return 2

class RoleBass(RoleBehavior):
    name = Role.BASS

    def choose_octave(self):
        oct = [octaves.Octave.OCTAVE_1, octaves.Octave.OCTAVE_2]
        return octaves.choose_octave(self.rng, oct)

    def adjust_velocity(self, velocity: int) -> int:
        return min(127, velocity + 5)
    
    def generate_rhythm(self, context):
        pattern = [(1.0, False)] * int(context.measure_duration)
        return RhythmicPattern(pattern)
    
    def phrase_length(self):
        return 8


class RolePad(RoleBehavior):
    name = Role.PAD

    def choose_octave(self):
        oct = [octaves.Octave.OCTAVE_3, octaves.Octave.OCTAVE_4]
        return octaves.choose_octave(self.rng, oct)

    def adjust_velocity(self, velocity: int) -> int:
        return max(20, velocity - 10)
    
    def generate_rhythm(self, context):
        pattern = [(context.measure_duration, False)]
        return RhythmicPattern(pattern)
    
    def phrase_length(self):
        return 8


class RoleCountermelody(RoleBehavior):
    name = Role.COUNTERMELODY

    def choose_octave(self):
        oct = [octaves.Octave.OCTAVE_3, octaves.Octave.OCTAVE_4]
        return octaves.choose_octave(self.rng, oct)

    def adjust_velocity(self, velocity: int) -> int:
        return min(127, velocity + 5)
    
    def generate_rhythm(self, context):
        return RhythmicPattern.generate(context)
    
    def phrase_length(self):
        return 4


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
