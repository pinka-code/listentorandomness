from .base import Style, RoleSpec
from listener_to_randomness.midi.orchestration import Role
from listener_to_randomness.midi.instruments import InstrumentType
from listener_to_randomness.core.time_signature import TimeSignature

JAZZ_STYLE = Style(
    name="jazz",

    pattern_length_range=(2, 6),
    phrase_variation_prob=0.9,

    tempo_choices=[90, 110, 130, 150, 170],  # slow → fast swing

    time_signature_choices=[
        TimeSignature("4/4", 4, 4, "binary"),
        TimeSignature("3/4", 3, 4, "binary"),
    ],

    forms = [
        [("A", 8), ("A", 8), ("B", 8), ("A", 8)],  # AABA
    ],

    melodic_profile={
        "intervals": [-3, -2, -1, 0, 1, 2, 3, 4],
        "weights":   [2, 3, 4, 1, 4, 3, 2, 1],
        "start_degree_weight": {
            0: 4,
            2: 2,
            4: 3,
            6: 2
        }
    },

    rhythmic_profile={
        "duration_weights": {
            0.125: 0.4,
            0.25: 0.9,
            0.5: 1.6,
            0.75: 1.2,
            1.0: 0.6,
            1.5: 0.6,
            2.0: 0.2,
            4.0: 0.05
        },
        "rest_probability": 0.12,
        "syncopation_prob": 0.65
    },

    roles={

        Role.MELODY: RoleSpec(
            instruments=[
                InstrumentType.TRUMPET,
                InstrumentType.CLARINET,
                InstrumentType.TROMBONE,
            ]
        ),

        Role.COUNTERMELODY: RoleSpec(
            instruments=[
                InstrumentType.TROMBONE,
                InstrumentType.CLARINET,
                InstrumentType.FRENCH_HORN,
            ]
        ),

        Role.HARMONY: RoleSpec(
            instruments=[
                InstrumentType.ACOUSTIC_GRAND_PIANO,
                InstrumentType.ELECTRIC_GUITAR_JAZZ,
            ]
        ),

        Role.BASS: RoleSpec(
            instruments=[
                InstrumentType.ACOUSTIC_BASS,
                InstrumentType.ELECTRIC_BASS_FINGER,
            ]
        ),

        Role.PAD: RoleSpec(
            instruments=[
                InstrumentType.STRING_ENSEMBLE_1,
            ]
        ),
    },

    optional_roles={
        Role.COUNTERMELODY: 0.4,
        Role.PAD: 0.2,
    },
)