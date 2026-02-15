import mesure, rythme, nuances

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
    motif = generer_motif(config, rng)
    nuance_phrase = nuances.choisir_nuance(rng)

    for i in range(nb_mesures):
        if i > 0 and rng.random() < config.variation_phrase_prob:
            motif = varier_motif(motif, rng)

        time_depart = mesure.construire_mesure_avec_motif(
            instr,
            time_depart,
            duree_mesure,
            motif,
            config,
            rng,
            nuance_phrase=nuance_phrase
        )

    # Résolution tonique finale
    if rng.random() < config.prob_resolution_tonique:
        time_depart = mesure.ajouter_tonique(instr, time_depart, config, rng, nuance_phrase=nuance_phrase)

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
