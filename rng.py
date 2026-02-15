from abc import ABC, abstractmethod
import random

class RandomInterface(ABC):

    @abstractmethod
    def choice(self, seq):
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

    def randint(self, a, b):
        return self._random.randint(a, b)

    def random(self):
        return self._random.random()

class BiasedRandom(RandomInterface):

    def __init__(self, seed=None):
        self._random = random.Random(seed)

    def choice(self, seq):
        return seq[0]  # toujours premier élément

    def randint(self, a, b):
        return int(a + (b - a) * (self._random.random() ** 2))

    def random(self):
        return self._random.random() ** 2
