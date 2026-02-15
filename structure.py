import gammes
import tempo
import signature
from armature import Armature

def generer_structure(rng):
    tempo_nom, tempo_bpm = tempo.choisir_tempo_avec_nom(rng)
    armature_obj = Armature.choisir_armature(rng)
    nom_armature = armature_obj.name
    notes_gamme = gammes.generer_gamme(armature_obj)
    signature_nom, sig_num, sig_den, sig_type = signature.choisir_signature(rng)
    num_pistes = rng.randint(1, 5)
    duree_totale = rng.randint(30, 180)

    from config import MusicConfig
    return MusicConfig(
        armature_nom = nom_armature,
        notes_gamme = notes_gamme,
        tempo_nom=tempo_nom,
        tempo_bpm=tempo_bpm,
        signature_nom=signature_nom,
        signature_num=sig_num,
        signature_den=sig_den,
        signature_type=sig_type,
        num_pistes=num_pistes,
        duree_totale=duree_totale
    )
