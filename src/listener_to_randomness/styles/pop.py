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

    forms = [
        [("Intro", 4), ("Verse", 8), ("Chorus", 8), ("Verse", 8), ("Chorus", 8)],
        [("Verse", 8), ("Chorus", 8), ("Bridge", 8), ("Chorus", 8)],
    ],

    melodic_profile={
        "intervals": [-2, -1, 0, 1, 2],
        "weights":   [1, 5, 2, 5, 1],
        "start_degree_weight": {
            0: 7,
            4: 2,
            2: 1
        }
    },

    rhythmic_profile={
        "duration_weights": {
            0.125: 0.05,
            0.25: 0.4,
            0.5: 1.8,
            0.75: 0.3,
            1.0: 1.5,
            1.5: 0.1,
            2.0: 0.2,
            4.0: 0.05
        },
        "rest_probability": 0.03,
        "syncopation_prob": 0.1
    },

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