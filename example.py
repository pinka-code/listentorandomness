import pretty_midi
import random

# ========================
# 1️⃣ Définition des gammes
# ========================

# Gammes majeures simples (note = MIDI number modulo 12)
gammes = {
    "C_major": [0, 2, 4, 5, 7, 9, 11],   # Do, Ré, Mi, Fa, Sol, La, Si
    "G_major": [7, 9, 11, 0, 2, 4, 6],   # Sol, La, Si, Do, Ré, Mi, Fa#
    "A_minor": [9, 11, 0, 2, 4, 5, 7],   # La, Si, Do, Ré, Mi, Fa, Sol
    "E_minor": [4, 6, 7, 9, 11, 0, 2],   # Mi, Fa#, Sol, La, Si, Do, Ré
}

# Choix aléatoire de la gamme
gamme_name, gamme_notes = random.choice(list(gammes.items()))
print("Gamme choisie :", gamme_name)

# ========================
# 2️⃣ Paramètres globaux
# ========================
num_pistes = 3  # nombre de pistes/instruments
notes_per_piste = 16
time_step = 0.25  # durée de base (en secondes)

# ========================
# 3️⃣ Création du MIDI
# ========================
midi = pretty_midi.PrettyMIDI()

for piste in range(num_pistes):
    # Choix aléatoire de l'instrument
    instrument_num = random.randint(0, 127)
    instrument = pretty_midi.Instrument(program=instrument_num)
    print(f"Piste {piste+1} → Instrument MIDI {instrument_num}")

    time = 0.0

    for _ in range(notes_per_piste):
        # Choix d'une note dans la gamme
        note_base = random.choice(gamme_notes)
        octave = random.randint(4, 6)  # octaves 4 à 6
        midi_note_number = note_base + 12 * octave

        # Durée et vélocité aléatoires
        duration = random.choice([0.25, 0.5, 0.75, 1.0])
        velocity = random.randint(50, 100)

        # Création de la note
        midi_note = pretty_midi.Note(
            velocity=velocity,
            pitch=midi_note_number,
            start=time,
            end=time + duration
        )

        instrument.notes.append(midi_note)
        time += duration

    midi.instruments.append(instrument)

midi.write('generative_multi_instrument.mid')
print("MIDI généré ! 🎶")
