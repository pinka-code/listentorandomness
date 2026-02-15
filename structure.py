import gammes
import tempo

def generer_structure(rng):
    # Tempo
    tempo_nom, tempo_bpm = tempo.choisir_tempo_avec_nom(rng)

    # Gamme
    gamme_nom, gamme_notes = gammes.choisir_gamme(rng)

    # Nombre de pistes (1 à 5)
    num_pistes = rng.randint(1, 5)

    # Durée totale (30s à 180s)
    duree_totale = rng.randint(30, 180)

    from config import MusicConfig
    return MusicConfig(
        gamme_nom=gamme_nom,
        gamme_notes=gamme_notes,
        tempo_nom=tempo_nom,
        tempo_bpm=tempo_bpm,
        num_pistes=num_pistes,
        duree_totale=duree_totale
    )
