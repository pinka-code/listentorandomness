import instruments
from phrase import Phrase

class Piste:
    def __init__(self, config, rng):
        self.config = config
        self.rng = rng
        self.instr, self.famille = instruments.choisir_instrument(rng)
        self.phrases = []

    def generer_phrases(self):
        time = 0.0
        while time < self.config.duree_totale:
            p = Phrase(self.config, self.rng)
            self.phrases.append(p)
            time = p.jouer(self.instr, time)
