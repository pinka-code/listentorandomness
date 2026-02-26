import logging

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F",
              "F#", "G", "G#", "A", "A#", "B"]

logging.basicConfig(
    filename="midi_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filemode="w",
)

def midi_to_name(pitch):
    note = NOTE_NAMES[pitch % 12]
    octave = pitch // 12 - 1
    return f"{note}{octave}"

def debug_notes(midi, logger=None):
    """
    Debug notes directly from a PrettyMIDI object.
    Writes output to log file instead of printing.
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    if not midi.instruments:
        logger.debug("--- MIDI EVENTS (no instruments) ---")
        return

    logger.debug("--- MIDI EVENTS ---")

    for instrument in midi.instruments:
        instrument_name = instrument.name or "Unnamed Instrument"
        logger.debug(f"Instrument: {instrument_name}")

        notes_sorted = sorted(instrument.notes, key=lambda n: n.start)

        for n in notes_sorted:
            name = midi_to_name(n.pitch)
            logger.debug(
                f"start={n.start:6.2f} | "
                f"dur={n.end - n.start:6.2f} | "
                f"pitch={name:4} | "
                f"vel={n.velocity:3}"
            )


    logger.debug("-------------------")
