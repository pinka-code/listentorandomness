from note import Note

class Phrase:
    """
    Responsabilités :
    - Orchestrer plusieurs mesures
    - Appliquer variation du motif mélodique
    - Ajouter la note finale
    """

    def __init__(
        self,
        config,
        motif_melodique,
        motif_rythmique,
        nb_mesures,
        role,
        mesure_class,
        rng,
    ):
        self.config = config
        self.motif_melodique = motif_melodique
        self.motif_rythmique = motif_rythmique
        self.nb_mesures = nb_mesures
        self.role = role
        self.mesure_class = mesure_class
        self.rng = rng

    def _varier_motif(self, motif):
        return [
            degre + self.rng.choice([-1, 0, 1])
            for degre in motif
        ]

    def _ajouter_note_finale(self, notes, nuance):
        pitch, fraction_duree = self.role.choisir_note_finale()

        last_time = max(n.start + n.duration for n in notes)

        notes.append(
            Note(
                pitch=pitch,
                start=last_time,
                duration=fraction_duree,
                velocity=nuance,
            )
        )

    def jouer(self, time_depart: float, nuance: int):
        notes = []
        current_time = time_depart
        motif_courant = self.motif_melodique

        for i in range(self.nb_mesures):

            if i > 0 and self.rng.random() < self.config.variation_phrase_prob:
                motif_courant = self._varier_motif(motif_courant)

            mesure = self.mesure_class(
                self.config,
                motif_courant,
                self.motif_rythmique,
                self.role,
            )

            notes_mesure = mesure.jouer(current_time, nuance)

            notes.extend(notes_mesure)

            duree_mesure = sum(n.duration for n in notes_mesure)
            current_time += duree_mesure

        self._ajouter_note_finale(notes, nuance)

        return notes
