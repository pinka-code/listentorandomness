import pretty_midi  # type: ignore

from .track import Track
from listener_to_randomness.midi.orchestration import choose_instrument_for_role
from .roles import create_role
from listener_to_randomness.midi.orchestration import Role
from .musical_form import MusicalForm


class Composition:
    """
    Responsibilities:
    - Orchestrate the tracks
    - Create MIDI instruments
    - Instantiate musical roles
    - Assemble the final composition
    """

    def __init__(self, config, rng):
        self.config = config
        self.rng = rng
        self.form = MusicalForm(config, rng)
        self.tracks = []

    def _used_roles(self):
        roles = [Role.MELODY, Role.HARMONY, Role.BASS]

        if self.rng.random() < 0.5:
            roles.append(Role.COUNTERMELODY)

        if self.rng.random() < 0.3:
            roles.append(Role.PAD)

        return roles

    def generate(self):
        initial_tempo = self.form.sections[0].context.tempo_bpm

        midi = pretty_midi.PrettyMIDI(
            initial_tempo=initial_tempo
        )

        for role_name in self._used_roles():
            instrument = choose_instrument_for_role(
                self.rng,
                role_name,
            )
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

                track.generate_section(
                    section=section,
                    start_bar=current_bar,
                )

                current_bar += section.bars

            self.tracks.append(track)
            midi.instruments.append(instrument.midi)

        return midi
