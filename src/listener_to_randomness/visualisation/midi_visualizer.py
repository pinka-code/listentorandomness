import pretty_midi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import gridspec
import os
import networkx as nx
from collections import Counter

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

def plot_global_complexity_map(midi_path, output_path, time_bin=0.1):
    """
    Plot all instruments in one complexity map.

    X = rhythmic complexity (duration entropy)
    Y = melodic complexity (interval entropy)
    Color = harmonic density
    """

    pm = pretty_midi.PrettyMIDI(midi_path)
    instruments = [inst for inst in pm.instruments if inst.notes]

    if not instruments:
        print("No tracks with notes found.")
        return

    rhythmic_values = []
    melodic_values = []
    harmonic_values = []
    labels = []

    for inst in instruments:

        inst.notes.sort(key=lambda n: n.start)

        pitches = np.array([note.pitch for note in inst.notes])
        durations = np.array([note.end - note.start for note in inst.notes])

        if len(pitches) < 2:
            continue

        intervals = np.diff(pitches)
        melodic_complexity = shannon_entropy(intervals)

        rhythmic_complexity = shannon_entropy(np.round(durations, 2))

        harmonic_density = compute_harmonic_density(
            inst.notes,
            time_bin=time_bin
        )

        rhythmic_values.append(rhythmic_complexity)
        melodic_values.append(melodic_complexity)
        harmonic_values.append(harmonic_density)

        labels.append(inst.name or f"Program_{inst.program}")

    if not rhythmic_values:
        return

    plt.figure(figsize=(9, 7))

    scatter = plt.scatter(
        rhythmic_values,
        melodic_values,
        c=harmonic_values,
        cmap="viridis",
        s=200
    )

    plt.colorbar(scatter, label="Harmonic Density")

    for i, label in enumerate(labels):
        plt.text(
            rhythmic_values[i] + 0.02,
            melodic_values[i] + 0.02,
            label,
            fontsize=8
        )

    plt.xlabel("Rhythmic Complexity (Entropy)")
    plt.ylabel("Melodic Complexity (Entropy)")
    plt.title("Global Complexity Map (All Instruments)")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"Saved global complexity map to {output_path}")

def compute_harmonic_density(notes, time_bin=0.1):
    """
    Compute average number of simultaneous notes (polyphony).
    """
    if not notes:
        return 0.0

    max_time = max(note.end for note in notes)
    bins = np.arange(0, max_time + time_bin, time_bin)

    density = []

    for t in bins:
        active = sum(1 for note in notes if note.start <= t < note.end)
        density.append(active)

    return np.mean(density)

def analyze_midi_tracks(midi_path, output_dir="midi_analysis", time_bin=0.1):
    """
    Analyze each track of a MIDI file and generate multiple plots per instrument.
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

        inst.notes.sort(key=lambda n: n.start)

        times = np.array([note.start for note in inst.notes])
        pitches = np.array([note.pitch for note in inst.notes])
        velocities = np.array([note.velocity for note in inst.notes])
        durations = np.array([note.end - note.start for note in inst.notes])

        plot_melody_contour(times, pitches, inst_name, inst_dir)
        plot_pitch_histogram(pitches, inst_name, inst_dir)
        plot_duration_histogram(durations, inst_name, inst_dir)
        plot_rhythmic_density(times, inst_name, inst_dir, time_bin)
        plot_velocity_over_time(times, pitches, velocities, inst_name, inst_dir)

        motifs = detect_repeated_motifs(pitches)
        save_motifs(motifs, inst_dir)

        plot_markov_transition(
            pitches,
            os.path.join(inst_dir, "markov_graph.png"),
            inst_name
        )

        analyze_entropy(
            pitches,
            durations,
            os.path.join(inst_dir, "entropy.txt"),
            inst_name,
            inst_dir
        )

        print(f"Saved analysis for {inst_name} in {inst_dir}")


def plot_melody_contour(times, pitches, inst_name, inst_dir):
    plt.figure(figsize=(12, 4))
    plt.plot(times, pitches, marker='o', linestyle='-')
    plt.xlabel("Time (s)")
    plt.ylabel("MIDI Pitch")
    plt.title(f"Melody contour - {inst_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(inst_dir, "melody.png"), dpi=150)
    plt.close()


def plot_pitch_histogram(pitches, inst_name, inst_dir):
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


def plot_duration_histogram(durations, inst_name, inst_dir):
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


def plot_rhythmic_density(times, inst_name, inst_dir, time_bin):
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


def plot_velocity_over_time(times, pitches, velocities, inst_name, inst_dir):
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


def detect_repeated_motifs(pitches, min_len=3, max_len=6):
    if len(pitches) < min_len:
        return []

    intervals = np.diff(pitches)
    motif_counts = Counter()

    for length in range(min_len, max_len + 1):
        for i in range(len(intervals) - length + 1):
            motif = tuple(intervals[i:i+length])
            motif_counts[motif] += 1

    repeated = [(motif, count)
                for motif, count in motif_counts.items()
                if count > 1]

    repeated.sort(key=lambda x: x[1], reverse=True)
    return repeated[:10]


def save_motifs(motifs, inst_dir):
    with open(os.path.join(inst_dir, "motifs.txt"), "w") as f:
        f.write("Top repeated interval motifs:\n\n")
        for motif, count in motifs:
            f.write(f"{motif} -> {count} occurrences\n")


def plot_markov_transition(pitches, output_path, instrument_name):
    if len(pitches) < 2:
        return

    transitions = Counter(zip(pitches[:-1], pitches[1:]))

    G = nx.DiGraph()
    for (p1, p2), weight in transitions.items():
        G.add_edge(p1, p2, weight=weight)

    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(G, seed=42)

    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]

    nx.draw(G, pos,
            with_labels=True,
            node_size=500,
            font_size=8,
            width=[w * 0.2 for w in weights],
            arrows=True)

    plt.title(f"Markov Transition Graph - {instrument_name}")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

# ==========================================================
# -------------------- ENTROPY -----------------------------
# ==========================================================

def shannon_entropy(values):
    """
    Compute Shannon entropy of a 1D array.
    """
    if len(values) == 0:
        return 0.0

    value, counts = np.unique(values, return_counts=True)
    probabilities = counts / counts.sum()

    return -np.sum(probabilities * np.log2(probabilities))


def compute_transition_entropy(pitches):
    """
    Entropy of pitch-to-pitch transitions.
    """
    if len(pitches) < 2:
        return 0.0

    transitions = list(zip(pitches[:-1], pitches[1:]))
    return shannon_entropy(transitions)


def analyze_entropy(pitches, durations, output_txt, inst_name, inst_dir):
    """
    Compute multiple entropy metrics and generate plots.
    """

    intervals = np.diff(pitches) if len(pitches) > 1 else []

    pitch_entropy = shannon_entropy(pitches)
    interval_entropy = shannon_entropy(intervals)
    duration_entropy = shannon_entropy(np.round(durations, 2))
    transition_entropy = compute_transition_entropy(pitches)

    with open(output_txt, "w") as f:
        f.write(f"Entropy analysis - {inst_name}\n\n")
        f.write(f"Pitch entropy: {pitch_entropy:.4f}\n")
        f.write(f"Interval entropy: {interval_entropy:.4f}\n")
        f.write(f"Duration entropy: {duration_entropy:.4f}\n")
        f.write(f"Transition entropy: {transition_entropy:.4f}\n")

    labels = [
        "Pitch",
        "Interval",
        "Duration",
        "Transition"
    ]

    values = [
        pitch_entropy,
        interval_entropy,
        duration_entropy,
        transition_entropy
    ]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.ylabel("Entropy (bits)")
    plt.title(f"Entropy profile - {inst_name}")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(os.path.join(inst_dir, "entropy_profile.png"), dpi=150)
    plt.close()
