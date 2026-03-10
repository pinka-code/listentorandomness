from abc import ABC, abstractmethod

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

    @abstractmethod
    def shuffle(self, seq):
        pass

    @abstractmethod
    def uniform(self, a: float, b: float) -> float:
        pass


class EntropySource(RandomInterface):
    pass

# Decorator
class RandomModifier(RandomInterface):

    def __init__(self, base_rng: RandomInterface):
        self.base_rng = base_rng