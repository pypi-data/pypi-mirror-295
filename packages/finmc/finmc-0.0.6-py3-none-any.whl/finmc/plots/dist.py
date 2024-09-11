import matplotlib.pyplot as plt
import numpy as np

from finmc.models.base import MCBase


def plot_distribution(
    model: MCBase,
    asset_name: str,
    asof: float = 1.0,
    xmax: float = 3.0,
):
    """Plot the progression of an asset in a model.

    Args:
        model: The model to use.
        asset_name: The name of the asset to plot.
        asof: The asof time (years) to plot the distribution.
        xmax: The max xrange in multiple of the mean value.

    Examples:
        >>> plot_distribution(model, "SPX", 1.0)
    """

    model.reset()
    model.advance(asof)
    spots = model.get_value(asset_name)

    # Plot distribution
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(spots, bins=100, density=True, alpha=0.3, color="r")

    ax.set_xlim(0, xmax * spots.mean())
    for side in ["left", "right", "top"]:
        ax.spines[side].set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_xlabel(asset_name)

    plt.show()


if __name__ == "__main__":
    from finmc.models.localvol import LVMC

    # create the dataset
    dataset = {
        "MC": {"PATHS": 100_000, "TIMESTEP": 1 / 10},
        "BASE": "USD",
        "ASSETS": {
            "USD": ("ZERO_RATES", np.array([[1.0, 0.04]])),
            "SPX": ("FORWARDS", np.array([[0.0, 5600], [1.0, 5700]])),
        },
        "LV": {
            "ASSET": "SPX",
            "VOL": 0.3,
        },
    }
    # create the model and plot the progression of short rate???
    model = LVMC(dataset)
    plot_distribution(model, "SPX", 1.0)
