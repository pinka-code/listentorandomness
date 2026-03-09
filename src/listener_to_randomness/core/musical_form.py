from . import tempo
from .key_signature import KeySignature
from .time_signature import TimeSignature
from .musical_context import MusicalContext
from .musical_section import MusicalSection

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
        section_key_signature = {}
        previous_key_signature = None

        for i, (name, bars) in enumerate(form):
            if name not in section_tempos:
                section_tempos[name] = tempo.choose(self.rng)
            tempo_bpm = section_tempos[name]

            if name in section_key_signature:
                key_signature = section_key_signature[name]
            else:
                if previous_key_signature is None:
                    key_signature = KeySignature.choose(self.rng)
                else:
                    key_signature = previous_key_signature.choose_neighbour_key(
                        self.rng, same_prob=0.7
                    )
                section_key_signature[name] = key_signature

            previous_key_signature = key_signature

            if name not in section_time_signature:
                section_time_signature[name] = TimeSignature.choose(self.rng)
            time_signature = section_time_signature[name]

            context = MusicalContext(key_signature, time_signature, tempo_bpm)
            sections.append(MusicalSection(name=name, bars=bars, context=context))

        return sections