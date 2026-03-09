from .instruments import Instrument
from .sound_design import SoundDesign
from enum import Enum

class Role(Enum):
    MELODY = "melody"
    COUNTERMELODY = "countermelody"
    HARMONY = "harmony"
    BASS = "bass"
    PAD = "pad"

def choose_instrument_for_role(ctx, role):
    role_spec = ctx.style.roles.get(role)

    if role_spec is None:
        raise ValueError(
            f"Role {role} not defined in style {ctx.style.name}"
        )

    instrument_type = ctx.rng.choice(role_spec.instruments)
    midi_instrument = instrument_type.create_pretty_midi()
    sound = SoundDesign(ctx.rng)

    return Instrument(
        midi=midi_instrument,
        name=instrument_type.label,
        sound=sound
    )