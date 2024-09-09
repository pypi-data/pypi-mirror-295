# Copyright (C) 2023 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher

import matplotlib.pyplot as plt
import numpy as np
import pytest

from trianglechain import LineChain
from trianglechain.params import get_samples


def test_basic_plots():
    samples1 = get_samples()
    samples2 = get_samples()
    prob = np.random.uniform(size=(len(samples1)))

    line = LineChain()
    line.contour_cl(samples1, color="r", label="test")
    line.contour_cl(samples2, color="b", label="test2", show_legend=True)

    line = LineChain()
    line.density_image(samples1)

    line = LineChain()
    line.scatter(samples1)

    line = LineChain()
    line.scatter_prob(samples1, prob=prob, colorbar=True)

    line = LineChain()
    line.scatter_density(samples1)
    plt.close("all")


def test_errors():
    samples = get_samples()
    with pytest.raises(ValueError):
        line = LineChain()
        line.scatter_prob(samples)


def test_scatter_probs():
    samples = get_samples()
    line = LineChain()

    prob = np.random.uniform(size=(len(samples))) - 1
    line.scatter_prob(samples, prob=prob, normalize_prob2D=True)
    line.scatter_prob(
        samples,
        prob=prob,
        normalize_prob2D=False,
        colorbar=True,
        cmap_vmin=0.1,
        cmap_vmax=0.9,
    )
    plt.close("all")


def test_orientation():
    samples = get_samples()
    line = LineChain(size=(1, 1), orientation="vertical")
    line.contour_cl(samples, color="r")
    x, y = line.fig.get_size_inches()
    assert x < y
    line = LineChain(size=(1, 1), orientation="horizontal")
    line.contour_cl(samples, color="r")
    x, y = line.fig.get_size_inches()
    assert x > y
    plt.close("all")


def test_n_points_scatter():
    samples = get_samples(10000)
    prob = np.ones(len(samples))
    line = LineChain()
    line.scatter(samples, n_points_scatter=10)
    line.scatter_density(samples, n_points_scatter=10)
    line.scatter_prob(samples, prob=prob, n_points_scatter=10)
    plt.close("all")


def test_alpha():
    samples = get_samples()
    line = LineChain()
    line.scatter(samples, alpha=0.5)
    line.scatter_density(samples, alpha2D=0.5)
    line.contour_cl(samples, alpha=0.5, alpha2D=0.5)
    plt.close("all")
