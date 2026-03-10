import pretty_midi  # type: ignore

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
        for role_name in self.style.choose_roles(self.rng, self.config.density_factor):
            instrument = choose_instrument_for_role(self.ctx, role_name, used_instruments)
            if instrument is None:
                continue
            print(f"Instrument: {instrument.name}")

            role = create_role(
                role_name=role_name,
                config=self.config,
                rng=self.rng
            )

            track = Track(
                config=self.config,
                rng=self.rng,
                role=role,
                instrument=instrument,
            )

            current_bar = 0
            for section in self.form.sections:
                print(f"Section {section.name} ({section.bars} bars) {section.context}")

                track.generate_section(section=section, start_bar=current_bar)
                current_bar += section.bars

            self.tracks.append(track)
            midi.instruments.append(instrument.midi)

        return midi