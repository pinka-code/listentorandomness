import pretty_midi  # type: ignore

class Note:
    def __init__(self, pitch, start, duration, velocity):
        self.pitch = pitch
        self.start = start
        self.duration = duration
        self.velocity = velocity

    def to_midi(self):
        return pretty_midi.Note(
            velocity=self.velocity,
            pitch=self.pitch,
            start=self.start,
            end=self.start + self.duration,
        )
