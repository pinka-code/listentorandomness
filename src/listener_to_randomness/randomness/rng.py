from abc import ABC, abstractmethod
import random

class RandomInterface(ABC):

    @abstractmethod
    def choice(self, seq):
        pass

    @abstractmethod
    def choice_weighted(self, seq, weights):
        pass

    @abstractmethod
    def randint(self, a: int, b: int) -> int:
        pass

    @abstractmethod
    def random(self) -> float:
        pass

class DefaultRandom(RandomInterface):

    def __init__(self, seed=None):
        self._random = random.Random(seed)

    def choice(self, seq):
        return self._random.choice(seq)
    
    def choice_weighted(self, seq, weights):
        return self._random.choices(seq, weights=weights, k=1)[0]

    def randint(self, a, b):
        return self._random.randint(a, b)

    def random(self):
        return self._random.random()

class BiasedRandom(RandomInterface):

    def __init__(self, seed=None):
        self._random = random.Random(seed)

    def choice(self, seq):
        return seq[0]  # always first element

    def randint(self, a, b):
        return int(a + (b - a) * (self._random.random() ** 2))

    def random(self):
        return self._random.random() ** 2
    
    def choice_weighted(self, seq, weights):
        if len(seq) != len(weights):
            raise ValueError("seq and weights must have same length")

        total = sum(weights)
        if total <= 0:
            raise ValueError("sum of weights must be > 0")

        r = self._random.random() * total
        cumulative = 0

        for item, weight in zip(seq, weights):
            cumulative += weight
            if r < cumulative:
                return item

        return seq[-1]
