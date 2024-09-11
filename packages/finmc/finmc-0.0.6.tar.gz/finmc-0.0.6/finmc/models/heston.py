# Monte Carlo Pricer for Heston Model

from math import sqrt

import numpy as np
from numpy.random import SFC64, Generator

from finmc.models.base import MCFixedStep
from finmc.utils.assets import Discounter, Forwards
from finmc.utils.mc import antithetic_normal


# Define a class for the state of a single asset Heston MC process
class HestonMC(MCFixedStep):
    def reset(self):
        self.n = self.dataset["MC"]["PATHS"]
        self.timestep = self.dataset["MC"]["TIMESTEP"]

        # create a random number generator
        self.rng = Generator(SFC64(self.dataset["MC"].get("SEED")))

        self.asset = self.dataset["HESTON"]["ASSET"]
        self.asset_fwd = Forwards(self.dataset["ASSETS"][self.asset])
        self.discounter = Discounter(
            self.dataset["ASSETS"][self.dataset["BASE"]]
        )

        self.heston_params = (
            self.dataset["HESTON"]["LONG_VAR"],
            self.dataset["HESTON"]["VOL_OF_VOL"],
            self.dataset["HESTON"]["MEANREV"],
            self.dataset["HESTON"]["CORRELATION"],
        )
        self.v0 = self.dataset["HESTON"]["INITIAL_VAR"]

        # We will reduce time spent in memory allocation by creating arrays in advance
        # and reusing them in the `advance` function which is called repeatedly.
        # though the values from one timestep are not reused in the next.
        self.tmp_vec = np.empty(self.n, dtype=np.float64)
        self.dz1_vec = np.empty(self.n, dtype=np.float64)
        self.dz2_vec = np.empty(self.n, dtype=np.float64)
        self.vol_vec = np.empty(self.n, dtype=np.float64)
        self.vplus_vec = np.empty(self.n, dtype=np.float64)

        # Initialize the arrays
        self.x_vec = np.zeros(self.n)  # processes x (log stock)
        self.v_vec = np.full(self.n, self.v0)  # processes v (variance)
        self.cur_time = 0

    def step(self, new_time):
        """Update x_vec, v_vec in place when we move simulation by time dt."""
        dt = new_time - self.cur_time

        (theta, vvol, meanrev, corr) = self.heston_params
        sqrtdt = sqrt(dt)

        # To improve preformance we will break up the operations into np.multiply,
        # np.add, etc. and use the `out` parameter to avoid creating temporary arrays.

        # calculate dz1 = normal(0,1) * sqrtdt
        antithetic_normal(self.rng, self.n, sqrtdt, self.dz1_vec)

        # calculate dz2 = normal(0,1) * sqrtdt * sqrt(1 - corr * corr) + corr * dz1
        corr_comp = sqrtdt * sqrt(1 - corr * corr)
        antithetic_normal(self.rng, self.n, corr_comp, self.dz2_vec)
        np.multiply(corr, self.dz1_vec, out=self.tmp_vec)  # second term
        np.add(self.dz2_vec, self.tmp_vec, out=self.dz2_vec)

        # vol = sqrt(max(v, 0))
        np.maximum(0.0, self.v_vec, out=self.vplus_vec)
        np.sqrt(self.vplus_vec, out=self.vol_vec)

        # update the current value of x (log Stock process)
        # first term: x -= vol * vol * dt/2
        np.divide(self.vplus_vec, 2, out=self.tmp_vec)
        np.multiply(self.tmp_vec, dt, out=self.tmp_vec)
        np.subtract(self.x_vec, self.tmp_vec, out=self.x_vec)

        # second term: x += vol * dz1
        np.multiply(self.vol_vec, self.dz1_vec, out=self.tmp_vec)
        np.add(self.x_vec, self.tmp_vec, out=self.x_vec)

        # update the current value of v (variance process)
        # first term: v += meanrev * (theta - v) * dt
        np.subtract(theta, self.v_vec, out=self.tmp_vec)
        np.multiply(self.tmp_vec, (meanrev * dt), out=self.tmp_vec)
        np.add(self.v_vec, self.tmp_vec, out=self.v_vec)

        # second term: v += vvol * vol * dz2
        np.multiply(vvol, self.vol_vec, out=self.tmp_vec)
        np.multiply(self.tmp_vec, self.dz2_vec, out=self.tmp_vec)
        np.add(self.v_vec, self.tmp_vec, out=self.v_vec)

        self.cur_time = new_time

    def get_value(self, unit):
        """Return the value of the unit at the current time."""
        if unit == self.asset:
            return self.asset_fwd.forward(self.cur_time) * np.exp(self.x_vec)

    def get_df(self):
        return self.discounter.discount(self.cur_time)
