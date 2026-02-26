from listener_to_randomness.midi.note import Note

class Measure:
    """
    Responsibilities:
    - Generate the notes of a measure
    - Apply melodic + rhythmic pattern
    - Delegate pitch and velocity decisions to the Role
    """

    def __init__(self, config, melodic_pattern, rhythmic_pattern, role):
        self.config = config
        self.melodic_pattern = melodic_pattern
        self.rhythmic_pattern = rhythmic_pattern
        self.role = role

    def play(self, start_time: float, dynamic: int):
        notes = []
        current_time = start_time

        for index, (degree, dur_tuple) in enumerate(zip(self.melodic_pattern, self.rhythmic_pattern)):
            duration, is_rest = dur_tuple
            if is_rest:
                pass
            pitch = self.role.choose_pitch(degree, index)
            velocity = self.role.adjust_velocity(dynamic, index)

            notes.append(
                Note(
                    pitch=pitch,
                    start=current_time,
                    duration=duration,
                    velocity=velocity,
                )
            )

            current_time += duration

        return notes