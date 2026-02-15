import mesure, nuances, rythme

class Phrase:
    def __init__(self, config, rng):
        """
        Initialise une phrase avec :
        - config : MusicConfig
        - rng : générateur random
        """
        self.config = config
        self.rng = rng
        self.nb_mesures = rng.randint(config.longueur_phrase_min, config.longueur_phrase_max)
        self.motif = self.generer_motif()
        self.motif_rythmique = self.generer_motif_rythmique()
        self.nuance = nuances.choisir_nuance(rng)

    def generer_motif(self):
        """Génère le motif mélodique de la phrase"""
        motif = []

        for _ in range(4):  # 4 notes par mesure
            degre = self.rng.randint(0, len(self.config.notes_gamme)-1)
            motif.append(degre)

        return motif

    def generer_motif_rythmique(self):
        """Génère le motif rythmique de la phrase"""
        duree_mesure = mesure.calculer_duree(self.config.signature_num, self.config.signature_den)
        return rythme.generer_motif_rythmique(duree_mesure, self.rng)
    
    def jouer(self, instr, time_depart):
        for i in range(self.nb_mesures):
            motif_courant = self.motif
            if i > 0 and self.rng.random() < self.config.variation_phrase_prob:
                motif_courant = self.varier_motif()

            m = mesure.Mesure(motif_courant, self.motif_rythmique, self.config, self.rng)
            time_depart = m.jouer(instr, time_depart, self.nuance)

        # résolution tonique
        if self.rng.random() < self.config.prob_resolution_tonique:
            time_depart = mesure.ajouter_tonique(instr, time_depart, self.config, self.rng, fraction_duree=0.5, nuance_phrase=self.nuance)

        return time_depart

    def varier_motif(self):
        """Retourne une version légèrement modifiée du motif"""
        nouveau = self.motif.copy()

        index = self.rng.randint(0, len(nouveau)-1)
        nouveau[index] = self.rng.randint(0, len(nouveau)-1)

        return nouveau
