from .base import Style, RoleSpec
from listener_to_randomness.midi.orchestration import Role
from listener_to_randomness.midi.instruments import InstrumentType
from listener_to_randomness.core.time_signature import TimeSignature

CLASSICAL_STYLE = Style(
    name="classical",

    pattern_length_range=(1, 4),
    phrase_variation_prob=0.6,

    tempo_choices=[50, 70, 90, 110],  # LARGO, ADAGIO, ANDANTE, MODERATO

    time_signature_choices=[
        TimeSignature("4/4", 4, 4, "binary"),
        TimeSignature("3/4", 3, 4, "binary"),
        TimeSignature("2/4", 2, 4, "binary"),
    ],

    roles={

        Role.MELODY: RoleSpec(
            instruments=[
                InstrumentType.VIOLIN,
                InstrumentType.FLUTE,
                InstrumentType.OBOE,
                InstrumentType.CLARINET,
            ]
        ),

        Role.COUNTERMELODY: RoleSpec(
            instruments=[
                InstrumentType.VIOLA,
                InstrumentType.CLARINET,
                InstrumentType.FRENCH_HORN,
                InstrumentType.BASSOON,
            ]
        ),

        Role.HARMONY: RoleSpec(
            instruments=[
                InstrumentType.ACOUSTIC_GRAND_PIANO,
                InstrumentType.STRING_ENSEMBLE_1,
                InstrumentType.CHURCH_ORGAN,
            ]
        ),

        Role.BASS: RoleSpec(
            instruments=[
                InstrumentType.CELLO,
                InstrumentType.CONTRABASS,
                InstrumentType.BASSOON,
            ]
        ),

        Role.PAD: RoleSpec(
            instruments=[
                InstrumentType.STRING_ENSEMBLE_1,
            ]
        ),
    },

    optional_roles={
        Role.COUNTERMELODY: 0.5,
        Role.PAD: 0.3,
    },
)