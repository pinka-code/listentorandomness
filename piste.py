from phrase import Phrase
from note import Note

class Piste:
    """
    Responsabilité :
    - Générer des phrases successives
    - Remplir l'instrument avec les notes produites
    - Respecter la durée totale du morceau
    """

    def __init__(
        self,
        config,
        rng,
        role,
        instrument,
        nom_instrument,
        mesure_class,
    ):
        self.config = config
        self.rng = rng
        self.role = role
        self.instrument = instrument
        self.nom_instrument = nom_instrument
        self.mesure_class = mesure_class

    def _generer_motif(self):
        return [
            self.rng.randint(0, len(self.config.notes_gamme) - 1)
            for _ in range(self.rng.randint(
                self.config.longueur_phrase_min,
                self.config.longueur_phrase_max
            ))
        ]

    def _generer_rythme(self, taille):
        return [1.0 for _ in range(taille)]

    def generer(self):
        time = 0.0

        while time < self.config.duree_totale:
            motif_melodique = self._generer_motif()
            rythme = self._generer_rythme(len(motif_melodique))

            phrase = Phrase(
                config=self.config,
                motif_melodique=motif_melodique,
                motif_rythmique=rythme,
                nb_mesures=1,
                role=self.role,
                mesure_class=self.mesure_class,
                rng=self.rng,
            )

            notes = phrase.jouer(time_depart=time, nuance=80) #TODO config ici

            for note in notes:
                end_time = note.start + note.duration

                if end_time <= self.config.duree_totale:
                    self.instrument.notes.append(note.to_midi())

            if notes:
                time = max(n.start + n.duration for n in notes)
            else:
                break
