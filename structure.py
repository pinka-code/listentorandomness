import gammes
import tempo
import signature

def generer_structure(rng):
    tempo_nom, tempo_bpm = tempo.choisir_tempo_avec_nom(rng)
    gamme_nom, gamme_notes = gammes.choisir_gamme(rng)
    signature_nom, sig_num, sig_den, sig_type = signature.choisir_signature(rng)
    num_pistes = rng.randint(1, 5)
    duree_totale = rng.randint(30, 180)

    from config import MusicConfig
    return MusicConfig(
        gamme_nom=gamme_nom,
        gamme_notes=gamme_notes,
        tempo_nom=tempo_nom,
        tempo_bpm=tempo_bpm,
        signature_nom=signature_nom,
        signature_num=sig_num,
        signature_den=sig_den,
        signature_type=sig_type,
        num_pistes=num_pistes,
        duree_totale=duree_totale
    )
