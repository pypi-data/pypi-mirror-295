from math import sqrt

import numpy as np
from numpy.random import SFC64, Generator

from finmc.models.base import MCFixedStep
from finmc.utils.assets import Discounter, Forwards
from finmc.utils.mc import antithetic_normal


# Define a single asset Black Scholes process with a flat volatility
class BSMC(MCFixedStep):
    def reset(self):
        # fetch the model parameters from the dataset
        self.n = self.dataset["MC"]["PATHS"]
        self.timestep = self.dataset["MC"]["TIMESTEP"]

        self.asset = self.dataset["LV"]["ASSET"]
        self.asset_fwd = Forwards(self.dataset["ASSETS"][self.asset])
        self.vol = self.dataset["BS"]["VOL"]
        self.discounter = Discounter(
            self.dataset["ASSETS"][self.dataset["BASE"]]
        )

        # Initialize rng and any arrays
        self.rng = Generator(SFC64(self.dataset["MC"].get("SEED")))
        self.dz_vec = np.empty(self.n, dtype=np.float64)

        self.x_vec = np.zeros(self.n)  # process x (log stock)
        self.cur_time = 0

    def step(self, new_time):
        """Update x_vec in place when we move simulation by time dt."""

        dt = new_time - self.cur_time

        antithetic_normal(self.rng, self.n, self.vol * sqrt(dt), self.dz_vec)

        self.x_vec += (-self.vol * self.vol / 2.0) * dt + self.dz_vec

        self.cur_time = new_time

    def get_value(self, unit):
        """Return the value of the modeled asset at the current time."""
        if unit == self.asset:
            return self.asset_fwd.forward(self.cur_time) * np.exp(self.x_vec)

    def get_df(self):
        return self.discounter.discount(self.cur_time)


# Define a class for the state of a single asset BS Local Vol MC process
class LVMC(MCFixedStep):
    def reset(self):
        # fetch the model parameters from the dataset
        self.n = self.dataset["MC"]["PATHS"]
        self.timestep = self.dataset["MC"]["TIMESTEP"]

        self.asset = self.dataset["LV"]["ASSET"]
        self.asset_fwd = Forwards(self.dataset["ASSETS"][self.asset])
        self.vol = self.dataset["LV"]["VOL"]
        self.discounter = Discounter(
            self.dataset["ASSETS"][self.dataset["BASE"]]
        )

        # Create rng and tmp arrays
        self.rng = Generator(SFC64(self.dataset["MC"].get("SEED")))
        self.dz_vec = np.empty(self.n, dtype=np.float64)
        self.tmp = np.empty(self.n, dtype=np.float64)

        # Initialize the process
        self.x_vec = np.zeros(self.n)  # process x (log stock)
        self.cur_time = 0

    def step(self, new_time):
        """Update x_vec in place when we move simulation by time dt."""

        dt = new_time - self.cur_time

        if callable(self.vol):
            vol = self.vol((self.cur_time, self.x_vec))
        else:
            vol = self.vol

        # generate the random numbers and advance the log stock process
        antithetic_normal(self.rng, self.n, sqrt(dt), self.dz_vec)
        self.dz_vec *= vol

        # add drift to x_vec: - vol * vol * dt/ 2.0
        np.multiply(vol, vol, out=self.tmp)
        self.tmp *= -0.5 * dt
        self.x_vec += self.tmp
        # add the random part to x_vec
        self.x_vec += self.dz_vec

        self.cur_time = new_time

    def get_value(self, unit):
        """Return the value of the modeled asset at the current time."""
        if unit == self.asset:
            return self.asset_fwd.forward(self.cur_time) * np.exp(self.x_vec)

    def get_df(self):
        """Return the discount factors at the current time."""
        return self.discounter.discount(self.cur_time)
