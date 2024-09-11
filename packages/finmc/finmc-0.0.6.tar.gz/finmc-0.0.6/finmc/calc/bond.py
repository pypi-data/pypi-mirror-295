"""
Utility to calculate prices of bonds from a MC Simulation model.
"""

import numpy as np

from finmc.models.base import MCBase


def zcb_price_mc(
    maturity: float,
    asset_name: str,
    model: MCBase,
) -> float:
    """Calculate the price of a Zero Coupon Bond using MC Simulation.

    Args:
        maturity: The time to maturity of the bond in years.
        asset_name: The name of the asset.
        model: The model used to simulate the asset price.

    Returns:
        The price of the zero coupon bond.

    Examples:
        >>> price = zcb_price_mc(T, "USD", model)
    """

    model.reset()
    model.advance(maturity)
    df = model.get_df()

    if model.dataset.get("BASE") == asset_name:
        return df.mean()
    else:
        spots = model.get_value(asset_name)
        return (spots * df).mean()


if __name__ == "__main__":
    from finmc.models.hullwhite import HullWhiteMC

    dataset = {
        "MC": {
            "PATHS": 100_000,
            "TIMESTEP": 1 / 10,
        },
        "BASE": "USD",
        "ASSETS": {
            "USD": ("ZERO_RATES", np.array([[1.0, 0.04]])),
        },
        "HW": {
            "ASSET": "USD",
            "MEANREV": 0.1,
            "VOL": 0.03,
        },
    }

    model = HullWhiteMC(dataset)
    price = zcb_price_mc(
        maturity=1,
        asset_name="USD",
        model=model,
    )
    print(f"price = {price}")
