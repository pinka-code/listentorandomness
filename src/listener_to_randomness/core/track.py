from .phrase import Phrase
from . import dynamics
from . import melody_motif

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
        measure_class,
    ):
        self.config = config
        self.rng = rng
        self.role = role
        self.instrument = instrument
        self.instrument_name = instrument_name
        self.measure_class = measure_class

        self.section_themes = {}

    def _pattern_for_section(self, section_name):
        if section_name in self.section_themes:
            return self.section_themes[section_name]

        if section_name == "A":
            pattern = melody_motif.generate_pattern(self.config, self.rng)

        else:
            base = self.section_themes.get("A")

            if base:
                pattern = melody_motif.transform_pattern(base, self.rng)
            else:
                pattern = melody_motif.generate_pattern(self.config, self.rng)

        self.section_themes[section_name] = pattern

        return pattern

    def generate_section(self, section, start_bar):
        bar_duration = section.bar_duration(self.config)
        start_time = start_bar * bar_duration
        end_time = start_time + section.bars * bar_duration
        time = start_time
        melodic_pattern = self._pattern_for_section(section.name)

        while time < end_time:

            velocity = dynamics.choose_dynamic(self.rng)
            measure_count = self.role.phrase_length()

            phrase = Phrase(
                config=self.config,
                melodic_pattern=melodic_pattern,
                measure_count=measure_count,
                role=self.role,
                velocity=velocity,
                measure_class=self.measure_class,
                rng=self.rng,
            )

            notes = phrase.play(start_time=time)

            for note in notes:
                note_end = note.start + note.duration

                if note_end <= end_time:
                    self.instrument.notes.append(note.to_midi())

            if notes:
                time = max(n.start + n.duration for n in notes)
            else:
                break
