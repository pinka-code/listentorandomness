from .interface import RandomModifier
import math

# Add global biais to some values
class BiasedRandom(RandomModifier):
    def __init__(self, base_rng, bias_factor=5):
        self.base_rng = base_rng
        self.bias_factor = bias_factor

    def choice(self, seq):
        return self.base_rng.choice(seq)

    def choice_weighted(self, seq, weights):
        biased_weights = [w * self.bias_factor for w in weights]
        return self.base_rng.choice_weighted(seq, biased_weights)

    def randint(self, a, b):
        r = self.random()
        return a + int(r * (b - a + 1))

    def random(self):
        """
        Map r in [0,1) to a biased value in [0,1) according to bias_factor:
        - bias_factor < 1 → favors lower numbers
        - bias_factor = 1 → uniform
        - bias_factor > 1 → favors higher numbers
        """
        r = self.base_rng.random()
        if self.bias_factor == 1:
            return r
        elif self.bias_factor > 1:
            return r ** (1 / self.bias_factor)
        else:
            return 1 - (1 - r) ** (1 / (1 / self.bias_factor))

    def uniform(self, a, b):
        r = self.random()
        return a + (b - a) * r

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

    def _gauss01(self):
        """Return a Gaussian value in [0,1) clipped and normalized."""
        # Box-Muller transform
        x = self.base_rng.random()
        y = self.base_rng.random()
        z = math.sqrt(-2 * math.log(x)) * math.cos(2 * math.pi * y)
        # scale by mean/std and clip to [0,1]
        value = self.mean + z * self.std
        return min(max(value, 0), 1)

    def random(self):
        """Return a random float [0,1) following the Gaussian."""
        return self._gauss01()

    def choice(self, seq):
        """Pick an element biased by Gaussian over the sequence."""
        idx = int(self._gauss01() * len(seq))
        # Clip index
        idx = min(idx, len(seq)-1)
        return seq[idx]

    def choice_weighted(self, seq, weights):
        """Weighted choice with Gaussian bias applied to weights."""
        # Optional: multiply weights by Gaussian to bias
        g = self._gauss01()
        biased_weights = [w * g for w in weights]
        return self.base_rng.choice_weighted(seq, biased_weights)

    def randint(self, a, b):
        """Gaussian integer in [a,b]."""
        r = self._gauss01()
        return a + int(r * (b - a + 1))

    def uniform(self, a, b):
        """Gaussian float in [a,b]."""
        r = self._gauss01()
        return a + r * (b - a)

    def shuffle(self, seq):
        """Shuffle with Gaussian bias could be complex; fallback to base."""
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

    def _next_state(self, seq):
        """Compute the next state following the transition matrix."""
        if self.current_state is None:
            self.current_state = self.base_rng.choice(seq)
            return self.current_state

        weights = self.transition_matrix.get(self.current_state)
        if not weights:
            self.current_state = self.base_rng.choice(seq)
        else:
            self.current_state = self.base_rng.choice_weighted(seq, weights)
        return self.current_state

    def choice(self, seq):
        return self._next_state(seq)

    def choice_weighted(self, seq, weights):
        # Optionally, apply weights on top of Markov
        state = self._next_state(seq)
        return state

    def random(self):
        # If states are numeric, pick a float from [0,1) using weighted state
        if self.current_state is None:
            self.current_state = self._next_state(list(self.transition_matrix.keys()))
        # Map state index to float
        keys = list(self.transition_matrix.keys())
        idx = keys.index(self.current_state)
        return idx / max(len(keys)-1, 1)

    def randint(self, a, b):
        r = self.random()
        return a + int(r * (b - a + 1))

    def uniform(self, a, b):
        r = self.random()
        return a + r * (b - a)

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

    def _next_value(self, seq):
        if self.counter % self.period == 0:
            value = seq[0]  # accent
        else:
            value = self.base_rng.choice(seq)
        self.counter += 1
        return value

    def choice(self, seq):
        return self._next_value(seq)

    def choice_weighted(self, seq, weights):
        return self._next_value(seq)

    def random(self):
        # Map the choice to a [0,1) float (assuming seq numeric or ordinal)
        return self.counter / max(self.period, 1)

    def randint(self, a, b):
        r = self.random()
        return a + int(r * (b - a + 1))

    def uniform(self, a, b):
        r = self.random()
        return a + r * (b - a)

    def shuffle(self, seq):
        return self.base_rng.shuffle(seq)

    def fork(self, seed_offset=0):
        new_base = self.base_rng.fork(seed_offset)
        new_instance = RhythmicRandom(new_base, period=self.period)
        new_instance.counter = self.counter
        return new_instance
