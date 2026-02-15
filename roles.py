class RoleComportement:
    """Classe de base pour le comportement d'un rôle musical."""

    nom = "default"

    def choisir_degre(self, mesure, motif_idx):
        """Choisit le degré dans le motif pour cette mesure."""
        return mesure.motif[motif_idx % len(mesure.motif)]

    def choisir_octave(self, mesure):
        """Choisit l'octave pour cette note."""
        return mesure.rng.choice([3, 4])

    def ajuster_velocity(self, velocity):
        """Ajuste la vélocité selon le rôle."""
        return velocity

    def choisir_note_finale(self, mesure, config, rng):
        """Retourne (degre, octave, fraction_duree) pour la note finale."""
        degre = 0  # tonique par défaut
        octave = rng.choice([3, 4])
        fraction_duree = 0.5
        return degre, octave, fraction_duree


class RoleMelodie(RoleComportement):
    nom = "melodie"

    def choisir_octave(self, mesure):
        return mesure.rng.choice([4, 5])

    def ajuster_velocity(self, velocity):
        return min(127, velocity + 10)

    def choisir_note_finale(self, mesure, config, rng):
        degre = 0
        octave = rng.choice([4, 5])
        fraction_duree = 0.5
        return degre, octave, fraction_duree


class RoleBasse(RoleComportement):
    nom = "basse"

    def choisir_degre(self, mesure, motif_idx):
        return mesure.rng.choice([0, 4])  # tonique + quinte

    def choisir_octave(self, mesure):
        return mesure.rng.choice([1, 2])

    def ajuster_velocity(self, velocity):
        return min(127, velocity + 5)

    def choisir_note_finale(self, mesure, config, rng):
        degre = 0  # tonique
        octave = rng.choice([1, 2])
        fraction_duree = 0.5
        return degre, octave, fraction_duree


class RolePad(RoleComportement):
    nom = "pad"

    def choisir_octave(self, mesure):
        return mesure.rng.choice([3, 4])

    def ajuster_velocity(self, velocity):
        return max(20, velocity - 10)

    def choisir_note_finale(self, mesure, config, rng):
        degre = 0
        octave = rng.choice([3, 4])
        fraction_duree = 1.0
        return degre, octave, fraction_duree


class RoleContrechant(RoleComportement):
    nom = "contrechant"

    def choisir_octave(self, mesure):
        return mesure.rng.choice([3, 4])

    def ajuster_velocity(self, velocity):
        return min(127, velocity + 5)

    def choisir_note_finale(self, mesure, config, rng):
        degre = 0
        octave = mesure.rng.choice([3, 4])
        fraction_duree = 0.5
        return degre, octave, fraction_duree


def creer_role(role_nom: str):
    """Renvoie l'objet rôle correspondant au nom."""
    mapping = {
        "melodie": RoleMelodie(),
        "basse": RoleBasse(),
        "pad": RolePad(),
        "contrechant": RoleContrechant(),
    }
    return mapping.get(role_nom, RoleComportement())
