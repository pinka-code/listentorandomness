from dataclasses import dataclass
from . import tempo
from . import config

@dataclass
class MusicalSection:
    name: str
    bars: int
    tempo_name: str
    tempo_bpm: int

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

        for name, bars in form:
            if name not in section_tempos:
                section_tempos[name] = tempo.choose_tempo_with_name(self.rng)

            tempo_name, tempo_bpm = section_tempos[name]

            sections.append(
                MusicalSection(name, bars, tempo_name, tempo_bpm)
            )

        return sections