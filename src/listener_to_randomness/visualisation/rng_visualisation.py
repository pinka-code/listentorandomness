from typing import Optional
import matplotlib.pyplot as plt

from listener_to_randomness.randomness import create_random

def plot_random_distribution(
    output_file: str,
    generator: str = "default",
    count: int = 1000,
    bins: int = 20,
    seed: Optional[int] = None,
    **rng_kwargs,
):
    """
    Generate random numbers from a RNG and save their distribution plot.

    Parameters
    ----------
    output_file : str
        Path of the image file to save (png, jpg, etc.)
    generator : str
        RNG implementation (default, biased, markov, etc.)
    count : int
        Number of random values to generate
    bins : int
        Histogram bins
    seed : int
        RNG seed
    rng_kwargs :
        Extra arguments passed to create_random (bias_factor, transition_matrix, etc.)
    """

    rng = create_random(
        seed=seed,
        mode=generator,
        **rng_kwargs,
    )

    random_values = [rng.random() for _ in range(count)]

    plt.figure()
    plt.hist(random_values, bins=bins)

    plt.xlabel("Random value")
    plt.ylabel("Count")
    plt.title(f"Distribution of random values ({generator})")

    plt.xlim(0, 1)
    plt.grid(True)

    plt.savefig(output_file)
    plt.close()

    print(f"Distribution plot saved to {output_file}")

def plot_rng_correlation(output_file, seed: Optional[int] = None, generator="default", count=5000, **kwargs):
    """
    Trace random(n) vs random(n+1) pour visualiser les dépendances entre valeurs générées.

    Args:
        output_file (str): chemin du fichier pour sauvegarder le plot.
        generator (str): type de RNG ('default', 'biased', 'gaussian', 'markov', etc.)
        count (int): nombre de valeurs à générer.
        **kwargs: arguments supplémentaires pour l'implémentation (ex: bias_factor, period, transition_matrix)
    """
    from listener_to_randomness.randomness import create_random

    rng = create_random(seed=seed, mode=generator, **kwargs)

    values = [rng.random() for _ in range(count)]

    x = values[:-1]
    y = values[1:]

    plt.figure(figsize=(6,6))
    plt.scatter(x, y, s=1, alpha=0.5)
    plt.xlabel("random(n)")
    plt.ylabel("random(n+1)")
    plt.title(f"Correlation plot - {generator}")
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.grid(True)
    plt.savefig(output_file)
    plt.close()

    print(f"Correlation plot saved to {output_file}")
