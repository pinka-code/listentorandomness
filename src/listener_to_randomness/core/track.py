from .phrase import Phrase
from . import dynamics
from .melodic_pattern import MelodicPattern

class Track:
    """
    Responsibilities:
    - Generate successive phrases
    - Fill the instrument with the produced notes
    """

    def __init__(
        self,
        config,
        rng,
        role,
        instrument,
        instrument_name,
    ):
        self.config = config
        self.rng = rng
        self.role = role
        self.instrument = instrument
        self.instrument_name = instrument_name
        self.section_themes = {}

    def _pattern_for_section(self, section):
        section_name = section.name
        if section_name in self.section_themes:
            return self.section_themes[section_name]

        if section_name == "A":
            pattern = MelodicPattern.generate(self.config, section.context, self.rng)

        else:
            base = self.section_themes.get("A")

            if base:
                pattern = MelodicPattern.generate(self.config, section.context, self.rng)
            else:
                pattern = MelodicPattern.generate(self.config, section.context, self.rng)

        self.section_themes[section_name] = pattern

        return pattern

    def generate_section(self, section, start_bar):
        bar_duration = section.context.bar_duration
        section_start = start_bar * bar_duration

        melodic_pattern = self._pattern_for_section(section)

        current_bar = 0

        while current_bar < section.bars:
            velocity = dynamics.choose_dynamic(self.rng)

            phrase_len = min(
                self.role.phrase_length(),
                section.bars - current_bar
            )

            phrase = Phrase(
                config=self.config,
                context=section.context,
                melodic_pattern=melodic_pattern,
                measure_count=phrase_len,
                role=self.role,
                velocity=velocity,
                rng=self.rng
            )

            phrase_start = section_start + current_bar * bar_duration

            notes = phrase.play(phrase_start)

            for note in notes:
                self.instrument.notes.append(note.to_midi())

            current_bar += phrase_len
