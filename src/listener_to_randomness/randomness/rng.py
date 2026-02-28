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


class BasePythonRandom(RandomInterface):

    def __init__(self, random_impl):
        self._random = random_impl

    def choice(self, seq):
        return self._random.choice(seq)

    def choice_weighted(self, seq, weights):
        return self._random.choices(seq, weights=weights, k=1)[0]

    def randint(self, a, b):
        return self._random.randint(a, b)

    def random(self):
        return self._random.random()

class DeterministicRandom(BasePythonRandom):
    def __init__(self, seed):
        super().__init__(random.Random(seed))

class TimeSeedRandom(BasePythonRandom):
    def __init__(self):
        super().__init__(random.Random())

class EntropyRandom(BasePythonRandom):
    def __init__(self):
        super().__init__(random.SystemRandom())

class BiasedRandom(RandomInterface):

    def __init__(self, base_rng: RandomInterface, bias_factor=1.5):
        self.base_rng = base_rng
        self.bias_factor = bias_factor

    def choice(self, seq):
        return self.base_rng.choice(seq)

    def choice_weighted(self, seq, weights):
        biased_weights = [w * self.bias_factor for w in weights]
        return self.base_rng.choice_weighted(seq, biased_weights)

    def randint(self, a, b):
        return self.base_rng.randint(a, b)

    def random(self):
        return self.base_rng.random()

class GaussianRandom(RandomInterface):

    def __init__(self, base_rng: RandomInterface, mean=0.5, std=0.15):
        self.base_rng = base_rng
        self.mean = mean
        self.std = std

    def choice(self, seq):
        x = self.base_rng.random()
        y = self.base_rng.random()
        import math
        z = math.sqrt(-2 * math.log(x)) * math.cos(2 * math.pi * y)
        normalized = min(max(0.5 + z * self.std, 0), 1)
        idx = int(normalized * len(seq))
        return seq[idx]

    def choice_weighted(self, seq, weights):
        return self.base_rng.choice_weighted(seq, weights)

    def randint(self, a, b):
        return self.base_rng.randint(a, b)

    def random(self):
        return self.base_rng.random()
    
class MarkovRandom(RandomInterface):

    def __init__(self, base_rng: RandomInterface, transition_matrix):
        self.base_rng = base_rng
        self.transition_matrix = transition_matrix
        self.current_state = None

    def choice(self, seq):
        if self.current_state is None:
            self.current_state = self.base_rng.choice(seq)
            return self.current_state

        weights = self.transition_matrix.get(self.current_state)
        if not weights:
            return self.base_rng.choice(seq)

        self.current_state = self.base_rng.choice_weighted(seq, weights)
        return self.current_state

    def choice_weighted(self, seq, weights):
        return self.choice(seq)

    def randint(self, a, b):
        return self.base_rng.randint(a, b)

    def random(self):
        return self.base_rng.random()
    
class RhythmicRandom(RandomInterface):

    def __init__(self, base_rng: RandomInterface, period=4):
        self.base_rng = base_rng
        self.period = period
        self.counter = 0

    def choice(self, seq):
        if self.counter % self.period == 0:
            value = seq[0]  # accent
        else:
            value = self.base_rng.choice(seq)

        self.counter += 1
        return value

    def choice_weighted(self, seq, weights):
        return self.choice(seq)

    def randint(self, a, b):
        return self.base_rng.randint(a, b)

    def random(self):
        return self.base_rng.random()
    
class FractalRandom(RandomInterface):

    def __init__(self, seed=0.5, r=3.99):
        self.x = seed
        self.r = r

    def _next(self):
        self.x = self.r * self.x * (1 - self.x)
        return self.x

    def random(self):
        return self._next()

    def randint(self, a, b):
        return a + int(self._next() * (b - a + 1))

    def choice(self, seq):
        idx = int(self._next() * len(seq))
        return seq[idx]

    def choice_weighted(self, seq, weights):
        total = sum(weights)
        r = self._next() * total
        cumulative = 0
        for item, weight in zip(seq, weights):
            cumulative += weight
            if r < cumulative:
                return item
        return seq[-1]
