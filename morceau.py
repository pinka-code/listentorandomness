import pretty_midi
from piste import Piste
from orchestration import choisir_instrument_pour_role

class Morceau:
    def __init__(self, config, rng):
        self.config = config
        self.rng = rng
        self.pistes = []

    def generer(self):
        midi = pretty_midi.PrettyMIDI()
        midi._PrettyMIDI__initial_tempo = self.config.tempo_bpm

        roles_utilises = ["melodie", "harmonie", "basse"]

        if self.rng.random() < 0.5:
            roles_utilises.append("contrechant")

        if self.rng.random() < 0.3:
            roles_utilises.append("pad")

        for role in roles_utilises:
            instr, nom = choisir_instrument_pour_role(self.rng, role)
            piste = Piste(self.config, self.rng, role, instr, nom)
            piste.generer_phrases()
            midi.instruments.append(instr)

        return midi
