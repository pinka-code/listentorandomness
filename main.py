import pretty_midi  # type: ignore
import gammes, octaves, rythme, instruments, nuances, tempo

num_pistes = 3
notes_par_piste = 16

# Création du MIDI
midi = pretty_midi.PrettyMIDI()

# Choisir le tempo
nom_tempo, bpm = tempo.choisir_tempo_avec_nom()
print(f"Tempo choisi : {nom_tempo} → {bpm} BPM")
midi._PrettyMIDI__initial_tempo = bpm  # définit le tempo global du fichier MIDI

# Choisir la gamme une seule fois via le module
nom_gamme, notes_gamme = gammes.choisir_gamme()
print("Gamme choisie :", nom_gamme)

for piste_id in range(num_pistes):
    instr, famille = instruments.choisir_instrument()  # retourne un tuple
    print(f"Piste {piste_id+1} → Famille : {famille}, Instrument MIDI {instr.program}")

    time = 0.0
    for _ in range(notes_par_piste):
        if rythme.generer_silence():
            # silence
            time += rythme.choisir_duree()
            continue

        note_base = gammes.choisir_note(notes_gamme)
        octave = octaves.choisir_octave()
        pitch = note_base + 12 * octave
        duration = rythme.choisir_duree()
        velocity = nuances.choisir_nuance()

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
