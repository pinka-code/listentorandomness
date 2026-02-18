from note import Note

class Mesure:
    """
    Responsabilité :
    - Générer les notes d'une mesure
    - Appliquer motif mélodique + rythmique
    - Déléguer pitch et velocity au Role
    """

    def __init__(self, config, motif_melodique, motif_rythmique, role):
        self.config = config
        self.motif_melodique = motif_melodique
        self.motif_rythmique = motif_rythmique
        self.role = role

    def jouer(self, time_depart: float, nuance: int):
        notes = []
        current_time = time_depart

        for index, (degre, duree) in enumerate(
            zip(self.motif_melodique, self.motif_rythmique)
        ):
            pitch = self.role.choisir_pitch(degre, index)
            velocity = self.role.ajuster_velocity(nuance, index)

            notes.append(
                Note(
                    pitch=pitch,
                    start=current_time,
                    duration=duree,
                    velocity=velocity,
                )
            )

            current_time += duree

        return notes
