import pretty_midi  # type: ignore
import copy

from .track import Track
from listener_to_randomness.midi.orchestration import choose_instrument_for_role
from .roles import create_role
from .musical_form import MusicalForm
from .musical_context import MusicalContext
from listener_to_randomness.styles import STYLES


class Composition:
    """
    Responsibilities:
    - Choose the style of the piece
    - Orchestrate the tracks
    - Create MIDI instruments
    - Instantiate musical roles
    - Assemble the final composition
    """

    def __init__(self, config, rng):
        self.config = config
        self.rng = rng
        self.style = rng.choice(list(STYLES.values()))
        self.form = MusicalForm(config, rng, style=self.style)
        self.tracks = []
        self.ctx = None

    def generate(self):
        tempo = self.style.choose_tempo(self.rng)
        time_signature = self.style.choose_time_signature(self.rng)

        self.ctx = MusicalContext(
            rng=self.rng,
            style=self.style,
            key_signature=self.form.sections[0].context.key_signature,
            time_signature=time_signature,
            tempo_bpm=tempo,
        )

        midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)

        print(f"Style: {self.style.name}, Tempo: {tempo} BPM, Time Signature: {time_signature.name}")

        used_instruments = set()
        for idx, role_name in enumerate(self.style.choose_roles(self.rng, self.config.density_factor)):
            instrument = choose_instrument_for_role(self.ctx, role_name, used_instruments)
            if instrument is None:
                continue

            instrument_rng = self.rng.fork(seed_offset=idx)
            print(f"Instrument: {instrument.name}")

            role = create_role(
                role_name=role_name,
                config=self.config,
                rng=instrument_rng
            )

            track = Track(
                config=self.config,
                rng=instrument_rng,
                role=role,
                instrument=instrument,
            )

            current_bar = 0
            last_note_end = 0.0

            for section_idx, section in enumerate(self.form.sections):
                section_rng = instrument_rng.fork(seed_offset=section_idx + 1000)
                section_context = copy.deepcopy(section.context)
                section_context.rng = section_rng

                last_note_end = track.generate_section(
                    section=section,
                    start_bar=current_bar,
                    context=section_context,
                    last_note_end=last_note_end
                )

                current_bar += section.bars

            self.tracks.append(track)
            midi.instruments.append(instrument.midi)

        return midi