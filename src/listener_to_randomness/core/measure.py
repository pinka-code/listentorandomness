from listener_to_randomness.midi.sound_design import SoundDesign
from .dynamics import Dynamics
from .articulation import Articulation

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

    def play(self, start_time: float, dynamic: Dynamics, articulation: Articulation, sound_design: SoundDesign):
        notes = []
        current_time = start_time
        bar_duration = self.context.bar_duration
        melodic_index = 0
        degrees = self.melodic_pattern.degrees

        for duration, rest in self.rhythmic_pattern.pattern:
            degree = degrees[melodic_index % len(degrees)]
            melodic_index += 1

            if rest:
                current_time += duration
                continue

            pitch = self.role.choose_pitch(self.context.scale_notes, degree)
            pos = (current_time - start_time) / bar_duration
            base_velocity = dynamic.choose(pos)
            accent = Dynamics.accent_boost(pos)
            velocity = self.role.adjust_velocity(base_velocity + accent)

            articulated_notes = articulation.apply(
                pitch,
                current_time,
                duration,
                velocity
            )

            final_notes = []
            for note in articulated_notes:
                sd_notes = sound_design.apply(
                    pitch=note.pitch,
                    start=note.start,
                    duration=note.duration,
                    velocity=note.velocity
                )
                final_notes.extend(sd_notes)

            notes.extend(final_notes)
            current_time += duration

        return notes