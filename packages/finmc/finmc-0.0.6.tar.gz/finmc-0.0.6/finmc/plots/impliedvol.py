import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


def plot_iv(strikes, expirations, surface, atm_vols, fwds):
    """Plot the implied volatility surface and forward curve.

    Args:
        strikes (np.array): The strike prices.
        expirations (np.array): The expiration times.
        surface (np.array): The implied volatility surface.
        atm_vols (np.array): The ATM volatilities.
        fwds (np.array): The forward prices

    Examples:
        >>> plot_iv(strikes, expirations, surface, atm_vols, fwds)
    """

    X, Y = np.meshgrid(strikes, expirations)
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(6, 6))
    ax.plot_surface(
        X,
        Y,
        surface,
        cmap=cm.inferno,
        alpha=0.5,
    )
    # Add wireframes for each expiration
    ax.plot_wireframe(X, Y, surface, color="brown", rstride=1, cstride=0)

    (z0, z1) = ax.get_zlim()
    if z1 - z0 < 0.05:
        ax.set_zlim(z0, z0 + 0.05)

    ax.set_xlabel("Strike (K)")
    ax.set_ylabel("Maturity (years)")
    plt.show()

    # Add atm vol curve
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.plot(
        expirations, atm_vols, color="brown", label="Forward Curve", marker="o"
    )

    (y0, y1) = ax.get_ylim()
    if y1 - y0 < 0.05:
        ax.set_ylim(y0 - 0.01, y0 + 0.05)

    ax.set_xlabel("Maturity (years)")
    ax.set_ylabel("ATM Vol")
    plt.show()
