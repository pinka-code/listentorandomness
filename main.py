import rng, config
import composition

# Generator choice
random_generator = rng.DefaultRandom(seed=42)
# random_generator = rng.BiasedRandom(seed=42)

cfg = config.generate_structure(random_generator)

print("===== COMPOSITION CONFIGURATION =====")
print(f"Key signature: {cfg.key_name}")
print(f"Tempo: {cfg.tempo_name} → {cfg.tempo_bpm} BPM")
print(f"Time signature: {cfg.time_signature_name}")
print(f"Number of tracks: {cfg.num_tracks}")
print(f"Target total duration: {cfg.total_duration} sec")
print("=====================================")

part = composition.Composition(cfg, random_generator)
midi = part.generate()
midi.write('generative_structured.mid')
print("MIDI generated ! 🎶")
