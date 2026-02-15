from phrase import Phrase

class Piste:
    def __init__(self, config, rng, role, instrument, nom_instrument):
        self.config = config
        self.rng = rng
        self.role = role
        self.instr = instrument
        self.nom_instrument = nom_instrument

    def generer_phrases(self):
        time = 0.0
        while time < self.config.duree_totale:
            p = Phrase(self.config, self.rng, self.role, self.nom_instrument)
            time = p.jouer(self.instr, time)
