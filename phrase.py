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

        # Nombre de mesures dans la phrase
        self.nb_mesures = rng.randint(config.longueur_phrase_min, config.longueur_phrase_max)

        # Motif mélodique et rythmique
        self.motif = self.generer_motif()
        self.motif_rythmique = self.generer_motif_rythmique()

        # Nuance unique pour toute la phrase
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
        duree_mesure = mesure.calculer_duree_mesure(
            self.config.signature_num, self.config.signature_den
        )
        return rythme.generer_motif_rythmique(duree_mesure, self.rng)
    
    def jouer(self, instr, time_depart):
        """
        Remplit l'instrument avec la phrase à partir de time_depart
        """
        for i in range(self.nb_mesures):
            # possibilité de variation sur les mesures suivantes
            if i > 0 and self.rng.random() < self.config.variation_phrase_prob:
                motif_courant = self.varier_motif()
            else:
                motif_courant = self.motif

            duree_mesure = mesure.calculer_duree_mesure(
                self.config.signature_num, self.config.signature_den
            )

            time_depart = mesure.construire_mesure_avec_motif(
                instr,
                time_depart,
                duree_mesure,
                motif_courant,
                self.config,
                self.rng,
                motif_rythmique=self.motif_rythmique,
                nuance_phrase=self.nuance
            )

        # possibilité de résoudre la tonique à la fin de la phrase
        if self.rng.random() < self.config.prob_resolution_tonique:
            time_depart = mesure.ajouter_tonique(
                instr,
                time_depart,
                self.config,
                self.rng,
                nuance_phrase=self.nuance
            )

        return time_depart

    def varier_motif(self):
        """Retourne une version légèrement modifiée du motif"""
        nouveau = self.motif.copy()

        index = self.rng.randint(0, len(nouveau)-1)
        nouveau[index] = self.rng.randint(0, len(nouveau)-1)

        return nouveau
