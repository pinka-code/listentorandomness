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

        base_ctx = MusicalContext(
            rng=self.rng,
            style=self.style,
            key_signature=self.form.sections[0].context.key_signature,
            time_signature=time_signature,
            tempo_bpm=tempo,
        )

        midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)

        print(
            f"Style: {self.style.name}, "
            f"Tempo: {tempo} BPM, "
            f"Time Signature: {time_signature.name}"
        )

        used_instruments = set()

        roles = self.style.choose_roles(
            base_ctx.rng,
            self.config.density_factor
        )

        for idx, role_name in enumerate(roles):
            track_ctx = copy.deepcopy(base_ctx)
            track_ctx.rng = base_ctx.rng.fork(seed_offset=idx)

            instrument = choose_instrument_for_role(
                track_ctx,
                role_name,
                used_instruments
            )

            if instrument is None:
                continue

            print(f"Instrument: {instrument.name}")

            role = create_role(
                role_name=role_name,
                config=self.config,
                rng=track_ctx.rng
            )

            track = Track(
                config=self.config,
                role=role,
                instrument=instrument,
            )

            current_bar = 0
            last_note_end = 0.0

            for section_idx, section in enumerate(self.form.sections):
                section_ctx = copy.deepcopy(track_ctx)
                section_ctx.rng = track_ctx.rng.fork(seed_offset=1000 + section_idx)

                section_instance = copy.deepcopy(section)
                section_instance.context = section_ctx

                last_note_end = track.generate_section(
                    section=section_instance,
                    start_bar=current_bar,
                    last_note_end=last_note_end
                )

                current_bar += section.bars


            self.tracks.append(track)
            midi.instruments.append(instrument.midi)

        return midi
