import numpy as np


class UniformGridInterp:
    """Helper class to interpolate, when x-array is uniformly spaced.
    This avoids the cost of index search in arbitrary x-array."""

    def __init__(self, xmin=-3.0, xmax=3.0, dx=0.01):
        """Initialize the x-range and allocate some arrays.

        Args:
            xmin: minimum x value.
            xmax: maximum x value.
            dx: spacing between x values.
        """

        self.dx = dx
        self.xmin = xmin
        self.x_vec = np.arange(xmin, xmax + dx / 2, dx)
        self.xlen = len(self.x_vec)

        # Pre-allocate arrays
        self.slope = np.zeros(self.xlen)

    def interp(self, x_vec, y_vec, out):
        """Interpolate y_vec at x_vec and store the result in out.

        Args:
            x_vec: x values to interpolate at.
            y_vec: known y values for interpolator's stored grid (x_vec).
            out: pre-allocated destination array to store the result.
        """

        # Find the left index of the interval containing x: idx = floor((x - xmin) / dx)
        # Reusing the out array as a temp array, as it is the same shape
        np.subtract(x_vec, self.xmin, out=out)
        np.divide(out, self.dx, out=out)
        idx = out.astype(int)

        # Clip the index to [0, xlen - 1]
        np.clip(idx, 0, self.xlen - 1, out=idx)

        # get slope of y in each interval
        np.subtract(y_vec[1:], y_vec[:-1], out=self.slope[:-1])
        self.slope[-1] = self.slope[-2]
        np.divide(self.slope, self.dx, out=self.slope)

        # y = (x - left) * slope + left
        np.subtract(x_vec, self.x_vec[idx], out=out)  # x - left
        np.multiply(out, self.slope[idx], out=out)  # * slope
        np.add(out, y_vec[idx], out=out)  # + left


if __name__ == "__main__":
    interp = UniformGridInterp(xmin=-2.0, xmax=2.0, dx=1.0)
    y_vec = interp.x_vec * 10  # Some arbitrary function
    print("x=", interp.x_vec)
    print("y=", y_vec)

    new_x = np.array([-0.5, 0.5])
    new_y = new_x * 0  # pre-allocate
    interp.interp(new_x, y_vec, new_y)
    print("x=", new_x)
    print("y=", new_y)
