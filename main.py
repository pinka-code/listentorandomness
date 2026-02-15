import pretty_midi  # type: ignore
import rng, structure
import morceau

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

morceau.construire_morceau(
    midi,
    config,
    random_generator
)

midi.write('generative_structured.mid')
print("MIDI généré ! 🎶")
