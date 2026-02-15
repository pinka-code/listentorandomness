import pretty_midi  # type: ignore
import rng, structure, octaves, rythme, instruments, nuances

# Choix du générateur
random_generator = rng.DefaultRandom(seed=42)
# ou
# random_generator = rng.BiasedRandom(seed=42)

# Génération du setup global
config = structure.generer_structure(random_generator)

print("===== CONFIGURATION DU MORCEAU =====")
print(f"Tonalité : {config.gamme_nom}")
print(f"Tempo : {config.tempo_nom} → {config.tempo_bpm} BPM")
print(f"Signature rythmique : {config.signature_nom}")
print(f"Nombre de pistes : {config.num_pistes}")
print(f"Durée totale cible : {config.duree_totale} sec")
print("=====================================")

# Création du MIDI
midi = pretty_midi.PrettyMIDI()
midi._PrettyMIDI__initial_tempo = config.tempo_bpm
midi.time_signature_changes.append(
    pretty_midi.TimeSignature(
        config.signature_num,
        config.signature_den,
        0  # début du morceau
    )
)

for piste_id in range(config.num_pistes):

    instr, famille = instruments.choisir_instrument(random_generator)
    print(f"Piste {piste_id+1} → {famille}")

    time = 0.0

    while time < config.duree_totale:

        if rythme.generer_silence(random_generator):
            duration = rythme.choisir_duree(random_generator)
            time += duration
            continue

        note_base = random_generator.choice(config.gamme_notes)
        octave = octaves.choisir_octave(random_generator)

        pitch = note_base + 12 * octave
        duration = rythme.choisir_duree(random_generator)
        velocity = nuances.choisir_nuance(random_generator)

        if time + duration > config.duree_totale:
            duration = config.duree_totale - time

        note = pretty_midi.Note(
            velocity=velocity,
            pitch=pitch,
            start=time,
            end=time + duration
        )

        instr.notes.append(note)
        time += duration

    midi.instruments.append(instr)

midi.write('generative_structured.mid')
print("MIDI généré ! 🎶")
