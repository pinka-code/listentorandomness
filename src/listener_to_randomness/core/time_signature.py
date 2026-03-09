class TimeSignature:
    """
    Represents a musical time signature.
    """

    TIME_SIGNATURES = {
        "2/4": {"num": 2, "den": 4, "type": "binary"},
        "3/4": {"num": 3, "den": 4, "type": "binary"},
        "4/4": {"num": 4, "den": 4, "type": "binary"},
        "2/2": {"num": 2, "den": 2, "type": "binary"},
        "6/8": {"num": 6, "den": 8, "type": "ternary"},
        "9/8": {"num": 9, "den": 8, "type": "ternary"},
        "12/8": {"num": 12, "den": 8, "type": "ternary"},
    }

    def __init__(self, name: str, numerator: int, denominator: int, ts_type: str):
        self.name = name
        self.numerator = numerator
        self.denominator = denominator
        self.type = ts_type  # "binary" or "ternary"

    def __repr__(self):
        return f"<TimeSignature {self.name} ({self.type})>"

    @classmethod
    def choose(cls, rng):
        """
        Randomly choose a time signature.
        Returns a TimeSignature object.
        """
        name, data = rng.choice(list(cls.TIME_SIGNATURES.items()))
        return cls(name, data["num"], data["den"], data["type"])
    
    def measure_duration_quarters(self) -> float:
        """
        Duration of one measure in quarter-note units.
        (1.0 = quarter note)
        """
        return self.numerator * (4 / self.denominator)