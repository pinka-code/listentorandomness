import instruments, mesure

def construire_morceau(midi, config, rng):
    """
    Construit toutes les pistes du morceau
    """

    duree_mesure = mesure.calculer_duree_mesure(config.signature_num, config.signature_den)

    for piste_id in range(config.num_pistes):

        instr, famille = instruments.choisir_instrument(rng)
        print(f"Piste {piste_id+1} → {famille}")

        time = 0.0

        while time < config.duree_totale:
            time = mesure.construire_mesure(
                instr,
                time,
                duree_mesure,
                config,
                rng
            )

        midi.instruments.append(instr)
