from .phrase import Phrase
from .dynamics import Dynamics
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
    ):
        self.config = config
        self.rng = rng
        self.role = role
        self.instrument = instrument
        self.section_patterns = {}

    def _pattern_for_section(self, section, role):
        key = (section.name, role)
        if key in self.section_patterns:
            return self.section_patterns[key]

        pattern = MelodicPattern.generate(section.context, self.rng)
        self.section_patterns[key] = pattern
        return pattern

    def generate_section(self, section, start_bar, context=None):
        ctx = context or section.context

        bar_duration = ctx.bar_duration
        section_start = start_bar * bar_duration

        melodic_pattern = self._pattern_for_section(section, self.role)

        current_bar = 0
        previous_velocity = None

        while current_bar < section.bars:

            phrase_len = min(
                self.role.phrase_length(),
                section.bars - current_bar
            )

            dynamics = Dynamics(
                rng=ctx.rng,
                start_velocity=previous_velocity
            )

            phrase = Phrase(
                config=self.config,
                context=ctx,
                melodic_pattern=melodic_pattern,
                measure_count=phrase_len,
                role=self.role,
                dynamics=dynamics,
                sound_design=self.instrument.sound,
                rng=ctx.rng
            )

            phrase_start = section_start + current_bar * bar_duration

            notes = phrase.play(phrase_start)

            for note in notes:
                self.instrument.midi.notes.append(note.to_midi())
                previous_velocity = note.velocity

            current_bar += phrase_len
