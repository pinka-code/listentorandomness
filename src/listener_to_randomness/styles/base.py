from listener_to_randomness.core.time_signature import TimeSignature
from listener_to_randomness.core.tempo import choose as choose_tempo

class RoleSpec:
    def __init__(self, instruments, motif_generators=None):
        self.instruments = instruments
        self.motif_generators = motif_generators or []

class Style:
    def __init__(
        self,
        name,
        pattern_length_range,
        phrase_variation_prob,
        roles,
        optional_roles=None,
        tempo_choices=None,
        time_signature_choices=None,
    ):
        self.name = name

        self.pattern_length_min = pattern_length_range[0]
        self.pattern_length_max = pattern_length_range[1]

        self.phrase_variation_prob = phrase_variation_prob

        self.roles = roles

        self.core_roles = list(roles.keys())
        self.optional_roles = optional_roles or {}

        self.tempo_choices = tempo_choices  # can be None, then use global choose()
        self.time_signature_choices = time_signature_choices  # list of TimeSignature

    def choose_roles(self, rng):
        selected = list(self.core_roles)
        for role, prob in self.optional_roles.items():
            if rng.random() < prob:
                selected.append(role)
        return selected

    def choose_tempo(self, rng):
        if self.tempo_choices:
            return rng.choice(self.tempo_choices)
        return choose_tempo(rng)

    def choose_time_signature(self, rng):
        if self.time_signature_choices:
            return rng.choice(self.time_signature_choices)
        return TimeSignature.choose(rng)