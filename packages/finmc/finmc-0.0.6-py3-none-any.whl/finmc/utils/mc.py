"""
This module contains utilities for Monte Carlo simulation.
"""

import numpy as np


def antithetic_normal(rng, n, scale, out):
    """Generate antithetic normal random numbers into a preallocated array.

    Args:
        rng: a random number generator.
        n: the number of samples to generate (must be even).
        scale: scaling factor to apply.
        out: the destination array of size n.

    Example:
        >>> rng = np.random.default_rng()
        >>> n = 10
        >>> out = np.empty(n, dtype=np.float64)
        >>> antithetic_normal(rng, n, 100.0, out)
        >>> print(out)
        [ -3.81721881   3.43045846 -25.60449457  90.48543061 -12.57430504
        3.81721881  -3.43045846  25.60449457 -90.48543061  12.57430504]

    """

    assert n % 2 == 0, "Number of paths must be even"
    h = n >> 1  # divide by 2
    rng.standard_normal(h, out=out[0:h])
    np.multiply(scale, out[0:h], out=out[0:h])
    np.negative(out[0:h], out=out[h:])


if __name__ == "__main__":
    rng = np.random.default_rng()
    n = 10
    out = np.empty(n, dtype=np.float64)
    antithetic_normal(rng, n, 100.0, out)
    print(out)
