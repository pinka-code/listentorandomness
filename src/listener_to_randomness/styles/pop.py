from .base import Style, RoleSpec
from listener_to_randomness.midi.orchestration import Role
from listener_to_randomness.midi.instruments import InstrumentType
from listener_to_randomness.core.time_signature import TimeSignature

POP_STYLE = Style(
    name="pop",

    pattern_length_range=(2, 4),
    phrase_variation_prob=0.7,

    tempo_choices=[90, 100, 110, 120, 130],

    time_signature_choices=[
        TimeSignature("4/4", 4, 4, "binary"),
    ],

    roles={

        Role.MELODY: RoleSpec(
            instruments=[
                InstrumentType.LEAD_SQUARE,
                InstrumentType.BRIGHT_ACOUSTIC_PIANO,
                InstrumentType.FLUTE,
            ]
        ),

        Role.COUNTERMELODY: RoleSpec(
            instruments=[
                InstrumentType.ACOUSTIC_GUITAR_STEEL,
                InstrumentType.ELECTRIC_GUITAR_JAZZ,
            ]
        ),

        Role.HARMONY: RoleSpec(
            instruments=[
                InstrumentType.ACOUSTIC_GUITAR_STEEL,
                InstrumentType.ACOUSTIC_GRAND_PIANO,
            ]
        ),

        Role.BASS: RoleSpec(
            instruments=[
                InstrumentType.ELECTRIC_BASS_FINGER,
                InstrumentType.ACOUSTIC_BASS,
            ]
        ),

        Role.PAD: RoleSpec(
            instruments=[
                InstrumentType.PAD_NEW_AGE,
                InstrumentType.STRING_ENSEMBLE_1,
            ]
        ),
    },

    optional_roles={
        Role.COUNTERMELODY: 0.5,
        Role.PAD: 0.6,
    },
)