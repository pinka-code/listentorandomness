import random
from .interface import EntropySource

"""
Base RNG implementations for the generative music framework.

This module defines the fundamental random number generators (RNGs)
used throughout the system. They are categorized by type and
predictability.

RNG Classes:

| Class                  | RNG Type                | Predictable?                     | Notes / Usage |
|------------------------|------------------------|----------------------------------|----------------|
| DeterministicRandom    | PRNG                   | ✅ Fully predictable            | Fixed seed → reproducible, ideal for testing and debugging |
| TimeSeedRandom         | PRNG                   | ⚠️ Predictable if internal seed known | Seed based on system time → pseudo-random, not secure |
| SecureRandom           | CSPRNG                 | ❌ Unpredictable                 | Uses SystemRandom() → cryptographically secure, not reproducible, suitable for security purposes |
| FractalRandom          | Deterministic Chaos    | ✅ Predictable if seed known     | Logistic map-based → creates chaotic but reproducible musical patterns, not a standard PRNG |

Additional notes:

1. PRNG (Pseudo-Random Number Generator)
   - Deterministic algorithm.
   - Reproducible if the same seed is used.
   - Good for simulations, tests, and reversible generative music.

2. CSPRNG (Cryptographically Secure PRNG)
   - Deterministic algorithm but **unpredictable without knowledge of internal state**.
   - Used for security: passwords, tokens, keys.
   - Backend is the system's entropy pool (SystemRandom / secrets).

3. Deterministic Chaos
   - Generates mathematically chaotic sequences (e.g., logistic map).
   - Predictable if initial seed is known.
   - Ideal for creating complex musical patterns that are reproducible.
"""

class BasePythonRandom(EntropySource):
    def __init__(self, random_impl=None, seed=None):
        if random_impl is not None:
            self._random = random_impl
        else:
            self._random = random.Random(seed)

    def choice(self, seq):
        return self._random.choice(seq)

    def choice_weighted(self, seq, weights):
        return self._random.choices(seq, weights=weights, k=1)[0]

    def randint(self, a, b):
        return self._random.randint(a, b)

    def random(self):
        return self._random.random()
    
    def shuffle(self, seq):
        self._random.shuffle(seq)
        return seq

    def uniform(self, a, b):
        return self._random.uniform(a, b)
    
    def fork(self, seed_offset: int = 0):
        base_seed = int(self.random() * 1_000_000_000)
        new_seed = base_seed + seed_offset
        return self.__class__(seed=new_seed)

# Very small linear congruential generator (intentionally bad for demonstration)
class TinyRandom(BasePythonRandom):
    MODULUS = 64
    MULTIPLIER = 5
    INCREMENT = 1

    period = MODULUS

    def __init__(self, seed: int = 1):
        self.state = seed % self.MODULUS
        super().__init__(random.Random(seed))

    def random(self) -> float:
        self.state = (
            self.state * self.MULTIPLIER + self.INCREMENT
        ) % self.MODULUS

        return self.state / self.MODULUS

    def fork(self, seed_offset: int = 0):
        new_seed = (self.state + seed_offset) % self.MODULUS
        return TinyRandom(new_seed)

# Deterministic PRNG: fixed seed, fully reproducible
class DeterministicRandom(BasePythonRandom):
    def __init__(self, seed):
        super().__init__(random.Random(seed))

    def fork(self, seed_offset: int = 0):
        base_seed = int(self.random() * 1_000_000_000)
        new_seed = base_seed + seed_offset
        return DeterministicRandom(new_seed)

# Pseudo-random PRNG: seed from system time, reproducible if state known
class TimeSeedRandom(BasePythonRandom):
    def __init__(self):
        super().__init__(random.Random())

# Cryptographically secure PRNG (CSPRNG): unpredictable, safe for security purposes
class SecureRandom(BasePythonRandom):
    def __init__(self):
        super().__init__(random.SystemRandom())

# Simple deterministic chaos (logistic map), predictable if initial seed known
class FractalRandom(EntropySource):
    def __init__(self, seed=0.5, r=3.99):
        self.x = seed
        self.r = r

    def _next(self):
        self.x = self.r * self.x * (1 - self.x)
        return max(0.0, min(self.x, 0.999999))

    def random(self):
        return self._next()

    def randint(self, a, b):
        val = a + int(self._next() * (b - a + 1))
        val = max(a, min(val, b))
        return val

    def choice(self, seq):
        idx = int(self._next() * len(seq))
        idx = min(idx, len(seq)-1)
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
    
    def shuffle(self, seq):
        for i in reversed(range(1, len(seq))):
            j = int(self._next() * (i + 1))
            seq[i], seq[j] = seq[j], seq[i]
        return seq
    
    def uniform(self, a, b):
        return a + self._next() * (b - a)
    
    def fork(self, seed_offset: float = 0.0):
        return FractalRandom(seed=self._next() + seed_offset, r=self.r)
