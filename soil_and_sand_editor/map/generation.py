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
    fade_u, fade_v = fade(xf), fade(yf)

    # Noise components
    noise_00 = gradient(p[p[xi] + yi], xf, yf)
    noise_01 = gradient(p[p[xi] + yi + 1], xf, yf - 1)
    noise_11 = gradient(p[p[xi + 1] + yi + 1], xf - 1, yf - 1)
    noise_10 = gradient(p[p[xi + 1] + yi], xf - 1, yf)

    # Combine noises
    x1 = liner_interpolation(noise_00, noise_10, fade_u)
    x2 = liner_interpolation(noise_01, noise_11, fade_u)

    return liner_interpolation(x1, x2, fade_v)


def liner_interpolation(noise_1, noise_2, x1):
    return noise_1 + x1 * (noise_2 - noise_1)


def fade(t):
    return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3


def gradient(h, x, y):
    vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    g = vectors[h % 4]
    return g[:, :, 0] * x + g[:, :, 1] * y


def create_perlin_str(
        start: int = 1, stop: int = 3, size: int = 200,
        seed: int = random.randint(0, 99999999)) -> str:
    lin_space = np.linspace(start, stop, size, endpoint=False)
    y, x = np.meshgrid(lin_space, lin_space)

    # Generate Perlin noise
    noise = perlin(x, y, seed=seed)

    noise = np.round(noise, 3)

    # Convert the noise array to a list of strings
    def row_to_string(row):
        return "".join(["#" if val > 0 else "~" for val in row])

    noise_strings = [row_to_string(row) for row in noise]

    build_string = "".join(noise_strings)

    return build_string
