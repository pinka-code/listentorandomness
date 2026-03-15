from .key_signature import KeySignature
from .musical_context import MusicalContext
from .musical_section import MusicalSection

class MusicalForm:
    def __init__(self, config, rng, style):
        self.config = config
        self.rng = rng
        self.style = style
        self.sections = self._generate_form()

    def _generate_form(self):
        form = self.rng.choice(self.style.forms)

        sections = []
        section_tempos = {}
        section_time_signatures = {}
        section_key_signatures = {}
        previous_key_signature = None

        for (name, bars) in enumerate(form):
            if name not in section_tempos:
                section_tempos[name] = self.style.choose_tempo(self.rng)
            tempo_bpm = section_tempos[name]

            if name in section_key_signatures:
                key_signature = section_key_signatures[name]
            else:
                if previous_key_signature is None:
                    key_signature = KeySignature.choose(self.rng)
                else:
                    key_signature = previous_key_signature.choose_neighbour_key(
                        self.rng, same_prob=0.7
                    )
                section_key_signatures[name] = key_signature
            previous_key_signature = key_signature

            if name not in section_time_signatures:
                section_time_signatures[name] = self.style.choose_time_signature(self.rng)
            time_signature = section_time_signatures[name]

            context = MusicalContext(
                rng=self.rng,
                style=self.style,
                key_signature=key_signature,
                time_signature=time_signature,
                tempo_bpm=tempo_bpm,
            )

            sections.append(MusicalSection(name=name, bars=bars, context=context))

        return sections