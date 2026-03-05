from dataclasses import dataclass


@dataclass
class MusicalSection:
    name: str
    bars: int


class MusicalForm:

    def __init__(self, config, rng):
        self.config = config
        self.rng = rng
        self.sections = self._generate_form()

    def _generate_form(self):

        forms = [
            [("A", 8), ("A", 8), ("B", 8), ("A", 8)],
            [("A", 8), ("B", 8), ("A", 8)],
            [("A", 8), ("B", 8), ("C", 8)],
        ]

        form = self.rng.choice(forms)
        total_bars = self.config.total_bars()
        base_total = sum(bars for _, bars in form)

        scale = total_bars / base_total if base_total else 1

        sections = []

        for name, bars in form:
            scaled_bars = max(4, int(round(bars * scale / 4)) * 4)
            sections.append(MusicalSection(name, scaled_bars))

        return sections