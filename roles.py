class RoleComportement:
    def choisir_degre(self, phrase, motif_idx):
        return phrase.motif[motif_idx % len(phrase.motif)]

    def choisir_octave(self, phrase):
        return phrase.rng.choice([3, 4])

    def ajuster_velocity(self, velocity):
        return velocity

class RoleMelodie(RoleComportement):

    def choisir_octave(self, phrase):
        return phrase.rng.choice([4, 5])

    def ajuster_velocity(self, velocity):
        return min(127, velocity + 10)

class RoleBasse(RoleComportement):

    def choisir_degre(self, phrase, motif_idx):
        return phrase.rng.choice([0, 4])  # tonique + quinte

    def choisir_octave(self, phrase):
        return phrase.rng.choice([1, 2])

    def ajuster_velocity(self, velocity):
        return min(127, velocity + 5)

class RolePad(RoleComportement):

    def choisir_octave(self, phrase):
        return phrase.rng.choice([3, 4])

    def ajuster_velocity(self, velocity):
        return max(20, velocity - 10)

def creer_role(role_nom):
    mapping = {
        "melodie": RoleMelodie(),
        "basse": RoleBasse(),
        "pad": RolePad(),
    }
    return mapping.get(role_nom, RoleComportement())
