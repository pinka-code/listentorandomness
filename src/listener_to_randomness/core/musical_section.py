from dataclasses import dataclass
from .musical_context import MusicalContext

@dataclass
class MusicalSection:
    name: str
    bars: int
    context: MusicalContext

