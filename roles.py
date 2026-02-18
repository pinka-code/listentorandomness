class RoleComportement:
    """
    Responsabilité :
    - Déterminer le pitch à partir d'un degré musical
    - Adapter la vélocité selon le contexte musical
    - Fournir la note de résolution finale
    - Encapsuler le comportement musical spécifique d'un rôle (mélodie, basse, accompagnement, etc.)
    """

    nom = "default"

    def __init__(self, config, rng=None):
        self.config = config
        self.rng = rng

    def choisir_degre(self, mesure=None, motif_idx=0):
        """Choisit le degré dans le motif (par défaut motif cyclique)."""
        if mesure:
            return mesure.motif[motif_idx % len(mesure.motif)]
        return 0

    def choisir_octave(self):
        """Octave par défaut (3 ou 4)."""
        return self.rng.choice([3, 4])

    def ajuster_velocity(self, velocity: int, idx=0) -> int:
        """Ajuste la vélocité selon le rôle (pas de changement par défaut)."""
        return velocity

    def choisir_pitch(self, degre: int, octave: int) -> int:
        """Retourne le pitch MIDI final en fonction du degré et de l'octave."""
        note_base = self.config.notes_gamme[degre % len(self.config.notes_gamme)]
        return note_base + 12 * octave

    def choisir_note_finale(self):
        """Retourne un tuple (pitch, fraction_duree) pour la note finale."""
        degre = 0
        octave = self.choisir_octave()
        fraction_duree = 0.5
        pitch = self.choisir_pitch(degre, octave)
        return pitch, fraction_duree


class RoleMelodie(RoleComportement):
    nom = "melodie"

    def choisir_octave(self):
        return self.rng.choice([4, 5])

    def ajuster_velocity(self, velocity: int, idx=0) -> int:
        return min(127, velocity + 10)

    def choisir_note_finale(self):
        degre = 0
        octave = self.choisir_octave()
        fraction_duree = 0.5
        pitch = self.choisir_pitch(degre, octave)
        return pitch, fraction_duree


class RoleBasse(RoleComportement):
    nom = "basse"

    def choisir_degre(self, mesure=None, motif_idx=0):
        return self.rng.choice([0, 4])  # tonique ou quinte

    def choisir_octave(self):
        return self.rng.choice([1, 2])

    def ajuster_velocity(self, velocity: int, idx=0) -> int:
        return min(127, velocity + 5)

    def choisir_note_finale(self):
        degre = 0
        octave = self.rng.choice([1, 2])
        fraction_duree = 0.5
        pitch = self.choisir_pitch(degre, octave)
        return pitch, fraction_duree


class RolePad(RoleComportement):
    nom = "pad"

    def choisir_octave(self):
        return self.rng.choice([3, 4])

    def ajuster_velocity(self, velocity: int, idx=0) -> int:
        return max(20, velocity - 10)

    def choisir_note_finale(self):
        degre = 0
        octave = self.choisir_octave()
        fraction_duree = 1.0
        pitch = self.choisir_pitch(degre, octave)
        return pitch, fraction_duree


class RoleContrechant(RoleComportement):
    nom = "contrechant"

    def choisir_octave(self):
        return self.rng.choice([3, 4])

    def ajuster_velocity(self, velocity: int, idx=0) -> int:
        return min(127, velocity + 5)

    def choisir_note_finale(self):
        degre = 0
        octave = self.choisir_octave()
        fraction_duree = 0.5
        pitch = self.choisir_pitch(degre, octave)
        return pitch, fraction_duree


def creer_role(role_nom: str, config=None, rng=None) -> RoleComportement:
    """Renvoie l'objet rôle correspondant au nom et l'instancie."""
    mapping = {
        "melodie": RoleMelodie,
        "basse": RoleBasse,
        "pad": RolePad,
        "contrechant": RoleContrechant,
    }
    RoleClass = mapping.get(role_nom.lower(), RoleComportement)
    return RoleClass(config=config, rng=rng)
