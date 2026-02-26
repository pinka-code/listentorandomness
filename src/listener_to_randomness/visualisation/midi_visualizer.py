import pretty_midi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import gridspec
import sys
import os

def plot_midi_pitch_time_velocity(midi_path, output_dir="src/listener_to_randomness/visualisation/plots", tracks_per_fig=2, track_height=4, y_margin=5):
    """
    Visualize MIDI composition and save figures:
        - Multiple figures if tracks > tracks_per_fig
        - Colorbar column (narrow, left)
        - Saved in 'output_dir' with filenames midi_plot_1.png, midi_plot_2.png...
    """
    pm = pretty_midi.PrettyMIDI(midi_path)
    instruments = [inst for inst in pm.instruments if inst.notes]

    if not instruments:
        print("No tracks with notes found.")
        return

    os.makedirs(output_dir, exist_ok=True)

    cmap = plt.cm.magma
    norm = plt.Normalize(0, 127)

    fig_count = 1
    for i in range(0, len(instruments), tracks_per_fig):
        batch = instruments[i:i + tracks_per_fig]
        n_tracks = len(batch)

        fig = plt.figure(figsize=(14, track_height * n_tracks))
        gs = gridspec.GridSpec(
            n_tracks,
            2,
            width_ratios=[0.03, 0.97],
            wspace=0.2,
            hspace=0.5
        )

        axes = []
        global_min_time = float("inf")
        global_max_time = 0

        for j, inst in enumerate(batch):
            ax = fig.add_subplot(gs[j, 1], sharex=axes[0] if axes else None)
            axes.append(ax)

            inst.notes.sort(key=lambda n: n.start)

            times = np.array([note.start for note in inst.notes])
            pitches = np.array([note.pitch for note in inst.notes])
            velocities = np.array([note.velocity for note in inst.notes])
            durations = np.array([note.end - note.start for note in inst.notes])

            for t, p, d, v in zip(times, pitches, durations, velocities):
                rect = Rectangle(
                    (t, p - 0.3),
                    d,
                    0.6,
                    facecolor=cmap(norm(v)),
                    edgecolor="none",
                    alpha=0.9
                )
                ax.add_patch(rect)

            ax.set_ylim(min(pitches) - y_margin, max(pitches) + y_margin)
            global_min_time = min(global_min_time, times.min())
            global_max_time = max(global_max_time, (times + durations).max())

            ax.set_ylabel("Pitch (MIDI)")
            instrument_name = inst.name or "Unnamed"
            ax.set_title(f"Track: {instrument_name}")

        for ax in axes:
            ax.set_xlim(global_min_time, global_max_time)
        axes[-1].set_xlabel("Time (seconds)")

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar_ax = fig.add_subplot(gs[:, 0])
        cbar = fig.colorbar(sm, cax=cbar_ax)
        cbar.set_label("Velocity", rotation=90, labelpad=10)
        cbar.ax.yaxis.set_label_position('left')
        cbar.ax.yaxis.set_ticks_position('left')
        cbar.ax.yaxis.set_tick_params(pad=5)

        file_path = os.path.join(output_dir, f"midi_plot_{fig_count}.png")
        fig.savefig(file_path, bbox_inches="tight", dpi=150)
        plt.close(fig)
        print(f"Saved {file_path}")
        fig_count += 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python midi_visualizer.py fichier.mid outputdir")
        sys.exit(1)

    midi_file = sys.argv[1]
    plot_midi_pitch_time_velocity(midi_file)