import pretty_midi
import matplotlib.pyplot as plt
import numpy as np
import sys

def plot_midi_pitch_time_velocity(midi_path):
    pm = pretty_midi.PrettyMIDI(midi_path)

    instruments = [inst for inst in pm.instruments if inst.notes]

    if not instruments:
        print("Aucune piste avec des notes.")
        return

    n_tracks = len(instruments)

    fig, axes = plt.subplots(
        n_tracks,
        1,
        figsize=(14, 3 * n_tracks),
        sharex=True
    )

    if n_tracks == 1:
        axes = [axes]

    for ax, instrument in zip(axes, instruments):

        times = np.array([note.start for note in instrument.notes])
        pitches = np.array([note.pitch for note in instrument.notes])
        velocities = np.array([note.velocity for note in instrument.notes])

        scatter = ax.scatter(
            times,
            pitches,
            c=velocities,
            cmap="viridis",
            alpha=0.8,
            edgecolors="black",
            linewidths=0.2
        )

        ax.set_ylabel("Pitch")

        instrument_name = instrument.name or "Unnamed"
        ax.set_title(f"{instrument_name}")

    axes[-1].set_xlabel("Temps (secondes)")

    cbar = fig.colorbar(scatter, ax=axes)
    cbar.set_label("Vélocité")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python midi_visualizer.py fichier.mid")
        sys.exit(1)

    midi_file = sys.argv[1]
    plot_midi_pitch_time_velocity(midi_file)