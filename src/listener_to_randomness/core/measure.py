from listener_to_randomness.midi.note import Note
from .dynamics import Dynamics

class Measure:
    """
    Responsibilities:
    - Generate the notes of a measure
    - Apply melodic + rhythmic pattern
    - Delegate pitch and velocity decisions to the Role
    """

    def __init__(self, config, context, melodic_pattern, rhythmic_pattern, role):
        self.config = config
        self.context = context
        self.melodic_pattern = melodic_pattern
        self.rhythmic_pattern = rhythmic_pattern
        self.role = role

    def play(self, start_time: float, dynamic: Dynamics):
        notes = []
        current_time = start_time
        bar_duration = self.context.bar_duration

        for degree, (duration, rest) in zip(
            self.melodic_pattern.degrees,
            self.rhythmic_pattern.pattern
        ):
            if not rest:
                pitch = self.role.choose_pitch(self.context.scale_notes, degree)
                pos = (current_time - start_time) / bar_duration
                base_velocity = dynamic.choose(pos)
                accent = Dynamics.accent_boost(pos)
                velocity = self.role.adjust_velocity(base_velocity + accent)

                notes.append(
                    Note(
                        pitch=pitch,
                        start=current_time,
                        duration=duration,
                        velocity=velocity
                    )
                )

            current_time += duration

        return notes