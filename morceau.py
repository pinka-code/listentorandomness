import pretty_midi  # type: ignore

from piste import Piste
from orchestration import choisir_instrument_pour_role
from roles import creer_role
from mesure import Mesure


class Morceau:
    """
    Responsabilité :
    - Orchestrer les pistes
    - Créer les instruments MIDI
    - Instancier les rôles
    - Assembler le morceau final
    """

    def __init__(self, config, rng):
        self.config = config
        self.rng = rng
        self.pistes = []

    def _roles_utilises(self):
        roles = ["melodie", "harmonie", "basse"]

        if self.rng.random() < 0.5:
            roles.append("contrechant")

        if self.rng.random() < 0.3:
            roles.append("pad")

        return roles

    def generer(self):
        midi = pretty_midi.PrettyMIDI(
            initial_tempo=self.config.tempo_bpm
        )

        for nom_role in self._roles_utilises():

            instrument, nom_instrument = choisir_instrument_pour_role(
                self.rng,
                nom_role,
            )

            role = creer_role(
                role_nom=nom_role,
                config=self.config,
                rng=self.rng,
            )

            piste = Piste(
                config=self.config,
                rng=self.rng,
                role=role,
                instrument=instrument,
                nom_instrument=nom_instrument,
                mesure_class=Mesure,
            )

            piste.generer()

            self.pistes.append(piste)
            midi.instruments.append(instrument)

        return midi
