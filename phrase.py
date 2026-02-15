import mesure, rythme

def construire_phrase(instr, time_depart, config, rng):
    """
    Construit une phrase musicale pour un instrument avec motif mélodique
    et motif rythmique réutilisable sur plusieurs mesures.

    - instr : PrettyMIDI Instrument
    - time_depart : temps de départ de la phrase (en beats)
    - config : configuration globale du morceau
    - rng : générateur random personnalisé
    """

    duree_mesure = mesure.calculer_duree_mesure(config.signature_num, config.signature_den)
    nb_mesures = rng.randint(config.longueur_phrase_min, config.longueur_phrase_max)
    motif_melodie = generer_motif(config, rng)
    motif_rythmique = rythme.generer_motif_rythmique(duree_mesure, rng)  # premier motif rythmique

    for i in range(nb_mesures):
        # variation mélodique ou rythmique
        if i > 0 and rng.random() < config.variation_phrase_prob:
            motif_melodie = varier_motif(motif_melodie, rng)
            motif_rythmique = rythme.generer_motif_rythmique(duree_mesure, rng)

        time_depart = mesure.construire_mesure_avec_motif(
            instr,
            time_depart,
            duree_mesure,
            motif_melodie,
            config,
            rng,
            motif_rythmique
        )

    # Résolution tonique finale
    if rng.random() < config.prob_resolution_tonique:
        time_depart = mesure.ajouter_tonique(instr, time_depart, config, rng)

    return time_depart

def generer_motif(config, rng):
    motif = []

    for _ in range(4):  # 4 notes par mesure
        degre = rng.randint(0, len(config.notes_gamme)-1)
        motif.append(degre)

    return motif

def varier_motif(motif, rng):
    nouveau = motif.copy()

    index = rng.randint(0, len(nouveau)-1)
    nouveau[index] = rng.randint(0, len(nouveau)-1)

    return nouveau
