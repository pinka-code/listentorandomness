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


def analyze_midi_tracks(midi_path, output_dir="midi_analysis", time_bin=0.1):
    """
    Analyze each track of a MIDI file and generate multiple plots per instrument:
        - Melody contour (pitch vs time)
        - Pitch histogram
        - Duration histogram
        - Rhythmic density (notes per time window)
        - Velocity over time

    Files are saved in a dedicated folder per instrument.

    Parameters:
        midi_path (str): path to the MIDI file
        output_dir (str): output directory
        time_bin (float): bin size (seconds) for rhythmic density histogram
    """
    pm = pretty_midi.PrettyMIDI(midi_path)
    instruments = [inst for inst in pm.instruments if inst.notes]

    if not instruments:
        print("No tracks with notes found.")
        return

    os.makedirs(output_dir, exist_ok=True)

    for inst in instruments:
        inst_name = inst.name or f"Instrument_{inst.program}"
        safe_name = "".join(c if c.isalnum() else "_" for c in inst_name)
        inst_dir = os.path.join(output_dir, safe_name)
        os.makedirs(inst_dir, exist_ok=True)

        times = np.array([note.start for note in inst.notes])
        pitches = np.array([note.pitch for note in inst.notes])
        velocities = np.array([note.velocity for note in inst.notes])
        durations = np.array([note.end - note.start for note in inst.notes])

        # Melody contour (Pitch vs Time)
        plt.figure(figsize=(12, 4))
        plt.plot(times, pitches, marker='o', linestyle='-')
        plt.xlabel("Time (s)")
        plt.ylabel("MIDI Pitch")
        plt.title(f"Melody contour - {inst_name}")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(inst_dir, "melody.png"), dpi=150)
        plt.close()

        # Pitch histogram
        plt.figure(figsize=(12, 4))
        plt.hist(pitches, bins=np.arange(0, 128) - 0.5,
                 color="skyblue", edgecolor="black")
        plt.xlabel("MIDI Pitch")
        plt.ylabel("Note count")
        plt.title(f"Pitch distribution - {inst_name}")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(inst_dir, "pitch_hist.png"), dpi=150)
        plt.close()

        # Duration histogram
        plt.figure(figsize=(12, 4))
        plt.hist(durations, bins=20,
                 color="lightgreen", edgecolor="black")
        plt.xlabel("Duration (s)")
        plt.ylabel("Note count")
        plt.title(f"Note duration distribution - {inst_name}")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(inst_dir, "duration_hist.png"), dpi=150)
        plt.close()

        # Rhythmic density
        bins = np.arange(0, times.max() + time_bin, time_bin)
        plt.figure(figsize=(12, 4))
        plt.hist(times, bins=bins,
                 color="salmon", edgecolor="black")
        plt.xlabel("Time (s)")
        plt.ylabel(f"Notes per {time_bin}s")
        plt.title(f"Rhythmic density - {inst_name}")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(inst_dir, "rhythm_density.png"), dpi=150)
        plt.close()

        # Velocity over time
        plt.figure(figsize=(12, 4))
        scatter = plt.scatter(times, pitches,
                              c=velocities,
                              cmap="magma",
                              s=velocities)
        plt.colorbar(scatter, label="Velocity")
        plt.xlabel("Time (s)")
        plt.ylabel("MIDI Pitch")
        plt.title(f"Velocity over time - {inst_name}")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(inst_dir, "velocity.png"), dpi=150)
        plt.close()

        print(f"Saved analysis for {inst_name} in {inst_dir}")