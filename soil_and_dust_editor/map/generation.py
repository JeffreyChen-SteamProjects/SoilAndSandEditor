import random

import numpy as np


def perlin(x, y, seed=0):
    # Permutation table
    np.random.seed(seed)
    p = np.arange(256, dtype=int)
    np.random.shuffle(p)
    p = np.stack([p, p]).flatten()

    # Coordinates of the top-left corner
    xi, yi = x.astype(int), y.astype(int)

    # Internal coordinates
    xf, yf = x - xi, y - yi

    # Fade factors
    u, v = fade(xf), fade(yf)

    # Noise components
    n00 = gradient(p[p[xi] + yi], xf, yf)
    n01 = gradient(p[p[xi] + yi + 1], xf, yf - 1)
    n11 = gradient(p[p[xi + 1] + yi + 1], xf - 1, yf - 1)
    n10 = gradient(p[p[xi + 1] + yi], xf - 1, yf)

    # Combine noises
    x1 = lerp(n00, n10, u)
    x2 = lerp(n01, n11, u)

    return lerp(x1, x2, v)


def lerp(a, b, x):
    """Linear interpolation"""
    return a + x * (b - a)


def fade(t):
    """6t^5 - 15t^4 + 10t^3"""
    return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3


def gradient(h, x, y):
    """Convert h to the right gradient vector and return the dot product with (x, y)"""
    vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    g = vectors[h % 4]
    return g[:, :, 0] * x + g[:, :, 1] * y


# Create a grid of points
lin = np.linspace(1, 2, 100, endpoint=False)
y, x = np.meshgrid(lin, lin)

# Generate Perlin noise
noise = perlin(x, y, seed=random.randint(0, 99999999))


# Convert the noise array to a list of strings
def row_to_string(row):
    return "".join(["#" if val > 0 else "~" for val in row])


noise_strings = [row_to_string(row) for row in noise]

# Print the Perlin noise as a list of strings
for row in noise_strings:
    print(row)
