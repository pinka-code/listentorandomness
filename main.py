import pretty_midi  # type: ignore
import rng, config
import morceau

# Choix du générateur
random_generator = rng.DefaultRandom(seed=42)
# random_generator = rng.BiasedRandom(seed=42)

cfg = config.generer_structure(random_generator)

print("===== CONFIGURATION DU MORCEAU =====")
print(f"Tonalité : {cfg.armature_nom}")
print(f"Tempo : {cfg.tempo_nom} → {cfg.tempo_bpm} BPM")
print(f"Signature rythmique : {cfg.signature_nom}")
print(f"Nombre de pistes : {cfg.num_pistes}")
print(f"Durée totale cible : {cfg.duree_totale} sec")
print("=====================================")

midi = pretty_midi.PrettyMIDI()
midi._PrettyMIDI__initial_tempo = cfg.tempo_bpm
midi.time_signature_changes.append(
    pretty_midi.TimeSignature(
        cfg.signature_num,
        cfg.signature_den,
        0  # début du morceau
    )
)

morceau.construire_morceau(
    midi,
    cfg,
    random_generator
)

midi.write('generative_structured.mid')
print("MIDI généré ! 🎶")
