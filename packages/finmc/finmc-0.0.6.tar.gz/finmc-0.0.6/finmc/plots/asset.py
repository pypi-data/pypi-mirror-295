import matplotlib.pyplot as plt
import numpy as np

from finmc.models.base import MCBase


def plot_asset(
    model: MCBase,
    asset_name: str,
    sample_idxs=np.arange(0, 3, 1),
    q_levels=np.linspace(0.02, 0.98, 25),
    times=np.linspace(0, 1, 101),
):
    """Plot the progression of an asset in a model.

    Args:
        model: The model to use.
        asset_name: The name of the asset to plot.
        sample_idxs (np.array, optional): The indices of the sample paths to plot in the foreground. Defaults to the first three.
        q_levels (np.array, optional): The quantiles to show in the background. Defaults to 25 levels from 2% to 98%.
        times (np.array, optional): The timesteps. Defaults to 1 year in 100 steps.

    Examples:
        >>> plot_asset(model, "SPX")
    """

    num_levels = len(q_levels)
    num_steps = len(times)

    samples = np.zeros((len(sample_idxs), num_steps))
    quantiles = np.zeros((len(q_levels), num_steps))

    # enumerate over the time steps and calculate the spot price
    model.reset()
    for i, t in enumerate(times):
        model.advance(t)
        spots = model.get_value(asset_name)
        quantiles[:, i] = np.quantile(spots, q_levels)
        samples[:, i] = spots[sample_idxs]

    fig, ax = plt.subplots(figsize=(8, 3))

    for i in range(num_levels >> 1):
        ax.fill_between(
            times,
            quantiles[i, :],
            quantiles[num_levels - 1 - i, :],
            color="darkred",
            alpha=1.5 / num_levels,
            edgecolor="none",
        )
    for sample in samples:
        ax.plot(times, sample)
    ax.set_xlabel("years")
    ax.set_ylabel(asset_name)
    ax.tick_params(axis="x", direction="in", pad=-15)

    for side in ["left", "bottom", "right", "top"]:
        ax.spines[side].set_visible(False)

    plt.show()


if __name__ == "__main__":
    from finmc.models.hullwhite import HullWhiteMC

    discount_data = (
        "ZERO_RATES",
        np.array([[0.5, 0.05], [1.0, 0.04], [3, 0.04]]),
    )

    dataset = {
        "MC": {"PATHS": 100_000, "TIMESTEP": 1 / 250, "SEED": 1},
        "BASE": "USD",
        "ASSETS": {"USD": discount_data},
        "HW": {
            "ASSET": "USD",
            "MEANREV": 0.1,
            "VOL": 0.03,
        },
    }
    # create the model and plot the progression of short rate???
    model = HullWhiteMC(dataset)
    plot_asset(model, "r")
