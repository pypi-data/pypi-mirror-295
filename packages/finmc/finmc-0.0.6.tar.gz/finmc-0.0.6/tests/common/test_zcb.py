"""
Testing ZCB for all models.
"""

import pytest
from pytest import approx

from finmc.calc.bond import zcb_price_mc
from finmc.utils.assets import Discounter
from tests.heston.dataset import data_heston_kruse
from tests.hullwhite.dataset import data_hwmc
from tests.localvol.dataset import (
    data_bsmc,
    data_lvmc,
    data_lvmc_fn,
    data_lvmc_grid,
)


@pytest.fixture(
    params=[
        data_bsmc,
        data_lvmc,
        data_lvmc_fn,
        data_lvmc_grid,
        data_heston_kruse,
        data_hwmc,
    ]
)
def data(request):
    return request.param()


@pytest.mark.parametrize("maturity", [0.1, 1.0, 3.0, 10.0])
def test_zcb(data, maturity):
    """Test the price of a zero coupon bond."""

    model_cls, dataset, _ = data
    if model_cls.__name__ == "HullWhiteMC":
        tol = 1e-3
    else:
        tol = 1e-5
        if maturity == 10.0:
            print("Skip.")
            return

    # Simulated Price of ZCB
    price = zcb_price_mc(
        maturity=maturity,
        asset_name="USD",
        model=model_cls(dataset),
    )

    # Get closed form price
    discounter = Discounter(dataset["ASSETS"][dataset["BASE"]])
    expected = discounter.discount(maturity)

    error = price - expected
    contract = f"ZCB {maturity:5.2f}"
    assert error == approx(0.0, abs=tol)

    print(f"{contract}: {price:11.6f} {expected:11.6f} {error * 1e4:7.2f}")
