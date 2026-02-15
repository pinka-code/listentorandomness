import pretty_midi  # type: ignore
import rng, gammes, octaves, rythme, instruments, nuances, tempo

num_pistes = 3
notes_par_piste = 16

# Création du MIDI
midi = pretty_midi.PrettyMIDI()

# Choix du générateur
random_generator = rng.DefaultRandom(seed=42)
# ou
# random_generator = rng.BiasedRandom(seed=42)

nom_tempo, bpm = tempo.choisir_tempo_avec_nom(random_generator)
print(f"Tempo choisi : {nom_tempo} → {bpm} BPM")
midi._PrettyMIDI__initial_tempo = bpm  # définit le tempo global du fichier MIDI

nom_gamme, notes_gamme = gammes.choisir_gamme(random_generator)
print("Gamme choisie :", nom_gamme)

for piste_id in range(num_pistes):
    instr, famille = instruments.choisir_instrument(random_generator)  # retourne un tuple
    print(f"Piste {piste_id+1} → Famille : {famille}, Instrument MIDI {instr.program}")

    time = 0.0
    for _ in range(notes_par_piste):
        if rythme.generer_silence(random_generator):
            # silence
            time += rythme.choisir_duree(random_generator)
            continue

        note_base = gammes.choisir_note(random_generator, notes_gamme)
        octave = octaves.choisir_octave(random_generator)
        pitch = note_base + 12 * octave
        duration = rythme.choisir_duree(random_generator)
        velocity = nuances.choisir_nuance(random_generator)

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
