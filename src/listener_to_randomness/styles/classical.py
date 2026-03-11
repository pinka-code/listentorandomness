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

    forms = [
        [("A", 8), ("A", 8), ("B", 8), ("A", 8)],  # AABA
        [("A", 8), ("B", 8), ("A", 8)],            # ABA
    ],

    melodic_profile={
        "intervals": [-2, -1, 0, 1, 2, 3, -3],
        "weights":   [1, 4, 3, 4, 2, 1, 1],
        "start_degree_weight": {
            0: 6,
            4: 2,
            2: 1
        }
    },

    rhythmic_profile={
        "duration_weights": {
            0.125: 0.05,
            0.25: 0.2,
            0.5: 1.0,
            0.75: 0.5,
            1.0: 1.3,
            1.5: 0.4,
            2.0: 0.6,
            4.0: 0.3
        },
        "rest_probability": 0.05,
        "syncopation_prob": 0.15
    },

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