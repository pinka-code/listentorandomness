"""
MIDI module for Listener To Randomness.

Provides:
- Instrument definitions
- Note representation
- Orchestration helpers
"""

# Import key items from submodules
from .instruments import InstrumentType
from .note import Note
from .orchestration import choose_instrument_for_role

# Public API
__all__ = [
    "InstrumentType",
    "Note",
    "choose_instrument_for_role",
]