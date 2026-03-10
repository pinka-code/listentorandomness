from .interface import RandomModifier
import math

# Add global biais to some values
class BiasedRandom(RandomModifier):
    def __init__(self, base_rng, bias_factor=1.5):
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
    
    def uniform(self, a, b):
        return self.base_rng.uniform(a, b)

    def shuffle(self, seq):
        return self.base_rng.shuffle(seq)
    
    def fork(self, seed_offset=0):
        new_base = self.base_rng.fork(seed_offset)
        return BiasedRandom(new_base, bias_factor=self.bias_factor)


# More probabilities to central values
class GaussianRandom(RandomModifier):
    def __init__(self, base_rng, mean=0.5, std=0.15):
        self.base_rng = base_rng
        self.mean = mean
        self.std = std

    def choice(self, seq):
        x = self.base_rng.random()
        y = self.base_rng.random()
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
    
    def uniform(self, a, b):
        return self.base_rng.uniform(a, b)

    def shuffle(self, seq):
        return self.base_rng.shuffle(seq)
    
    def fork(self, seed_offset=0):
        new_base = self.base_rng.fork(seed_offset)
        return GaussianRandom(new_base, mean=self.mean, std=self.std)


# Memory of precedent state    
class MarkovRandom(RandomModifier):

    def __init__(self, base_rng, transition_matrix):
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
    
    def uniform(self, a, b):
        return self.base_rng.uniform(a, b)

    def shuffle(self, seq):
        return self.base_rng.shuffle(seq)
    
    def fork(self, seed_offset=0):
        new_base = self.base_rng.fork(seed_offset)
        new_instance = MarkovRandom(new_base, self.transition_matrix)
        new_instance.current_state = self.current_state
        return new_instance
    
# Add periodicity
class RhythmicRandom(RandomModifier):

    def __init__(self, base_rng, period=4):
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
    
    def uniform(self, a, b):
        return self.base_rng.uniform(a, b)

    def shuffle(self, seq):
        return self.base_rng.shuffle(seq)
    
    def fork(self, seed_offset=0):
        new_base = self.base_rng.fork(seed_offset)
        new_instance = RhythmicRandom(new_base, period=self.period)
        new_instance.counter = self.counter
        return new_instance
