import pretty_midi
from piste import Piste

class Morceau:
    def __init__(self, config, rng):
        self.config = config
        self.rng = rng
        self.pistes = []

    def generer(self):
        midi = pretty_midi.PrettyMIDI()
        midi._PrettyMIDI__initial_tempo = self.config.tempo_bpm
        for i in range(self.config.num_pistes):
            piste = Piste(self.config, self.rng)
            print(f"Piste {piste.famille}")
            piste.generer_phrases()
            midi.instruments.append(piste.instr)
            self.pistes.append(piste)
        return midi
