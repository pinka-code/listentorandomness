import copy

class MusicalContext:
    def __init__(
        self,
        rng,
        style,
        key_signature,
        time_signature,
        tempo_bpm,
    ):
        self.rng = rng
        self.style = style

        self.key_signature = key_signature
        self.time_signature = time_signature
        self.tempo_bpm = tempo_bpm

    def __repr__(self):
        return (
            f"MusicalContext("
            f"key={self.key_signature}, "
            f"time={self.time_signature}, "
            f"tempo={self.tempo_bpm}, "
            f"scale={self.scale_notes})"
        )
    
    def __deepcopy__(self, memo):
        new = self.__class__.__new__(self.__class__)
        memo[id(self)] = new

        for k, v in self.__dict__.items():
            if k == "rng":
                setattr(new, k, v)  # ne pas copier le RNG
            else:
                setattr(new, k, copy.deepcopy(v, memo))

        return new

    @property
    def scale_notes(self):
        return self.key_signature.generate_scale()

    @property
    def measure_duration(self):
        return self.time_signature.measure_duration_quarters()

    @property
    def bar_duration(self) -> float:
        beat_duration = 60.0 / self.tempo_bpm
        beat_unit = 4 / self.time_signature.denominator
        return self.time_signature.numerator * beat_unit * beat_duration
