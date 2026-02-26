import pretty_midi  # type: ignore

from .track import Track
from listener_to_randomness.midi.orchestration import choose_instrument_for_role
from .roles import create_role
from listener_to_randomness.midi.orchestration import Role
from .measure import Measure


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
        self.tracks = []

    def _used_roles(self):
        roles = [Role.MELODY, Role.HARMONY, Role.BASS]

        if self.rng.random() < 0.5:
            roles.append(Role.COUNTERMELODY)

        if self.rng.random() < 0.3:
            roles.append(Role.PAD)

        return roles

    def generate(self):
        midi = pretty_midi.PrettyMIDI(
            initial_tempo=self.config.tempo_bpm
        )

        for role_name in self._used_roles():

            instrument, instrument_name = choose_instrument_for_role(
                self.rng,
                role_name,
            )
            print(f"Instrument: {instrument_name}")

            role = create_role(
                role_name=role_name,
                config=self.config,
                rng=self.rng,
            )

            track = Track(
                config=self.config,
                rng=self.rng,
                role=role,
                instrument=instrument,
                instrument_name=instrument_name,
                measure_class=Measure,
            )

            track.generate()

            self.tracks.append(track)
            midi.instruments.append(instrument)

        return midi
