import pretty_midi  # type: ignore
from listener_to_randomness.midi.note import Note

NOTE_DURATION = 0.5
CLARINET_PROGRAM = pretty_midi.instrument_name_to_program("Clarinet")

def random_to_pitch(r: float) -> int:
    """
    Map random float [0,1) to MIDI pitch.
    Range: C4 → C6
    """
    return 60 + int(r * 24)


def generate_rng_demo(rng, note_count=120, cycle_length=None):
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(
        program=CLARINET_PROGRAM
    )

    for i in range(note_count):
        r = rng.random()
        pitch = random_to_pitch(r)
        start = i * NOTE_DURATION

        velocity = 80
        duration = NOTE_DURATION

        if cycle_length is not None and i % cycle_length == 0:
            velocity = 120
            duration = NOTE_DURATION * 1.5

        note = Note(
            pitch=pitch,
            start=start,
            duration=duration,
            velocity=velocity,
        )

        instrument.notes.append(note.to_midi())

        print(f"{i:03d} random={r:.5f} pitch={pitch} velocity={velocity}")

    midi.instruments.append(instrument)

    return midi