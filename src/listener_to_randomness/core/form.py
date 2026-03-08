from dataclasses import dataclass
from . import tempo
from . import config
from .key_signature import KeySignature
from .time_signature import TimeSignature

@dataclass
class MusicalSection:
    name: str
    bars: int
    tempo_name: str
    tempo_bpm: int
    key_signature: KeySignature
    time_signature: TimeSignature

    def bar_duration(self, config: config.MusicConfig) -> float:
        beat_duration = 60.0 / self.tempo_bpm
        beat_unit = 4 / config.time_signature_den
        return config.time_signature_num * beat_unit * beat_duration


class MusicalForm:
    def __init__(self, config, rng):
        self.config = config
        self.rng = rng
        self.sections = self._generate_form()

    def _generate_form(self):
        forms = [
            [("A", 8), ("A", 8), ("B", 8), ("A", 8)],
            [("A", 8), ("B", 8), ("A", 8)],
            [("A", 8), ("B", 8), ("C", 8)],
        ]

        form = self.rng.choice(forms)

        sections = []
        section_tempos = {}
        section_time_signature = {}

        previous_key_signature = None

        for i, (name, bars) in enumerate(form):
            if name not in section_tempos:
                section_tempos[name] = tempo.choose_tempo_with_name(self.rng)
            tempo_name, tempo_bpm = section_tempos[name]

            if i == 0:
                key_signature = KeySignature.choose(self.rng)
            else:
                key_signature = previous_key_signature.choose_neighbour_key(self.rng, same_prob=0.7)

            previous_key_signature = key_signature

            if name not in section_time_signature:
                section_time_signature[name] = TimeSignature.choose(self.rng)
            time_signature = section_time_signature[name]

            sections.append(
                MusicalSection(name, bars, tempo_name, tempo_bpm, key_signature, time_signature)
            )

        return sections