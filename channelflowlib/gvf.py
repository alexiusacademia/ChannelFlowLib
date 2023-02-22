import math

from .constants import GRAVITY_G


def gradually_varied_flow_rectangular(x, dx, d0, Q, b, n, S0, z0):
    """
    Calculates the water surface elevation and flow depth at a specified location
    in a prismatic channel, using the gradually varied flow equations with the Manning
    equation for friction.

    Args:
        x (float): distance from the upstream end of the channel (m)
        dx (float): length of channel reach (m)
        d0 (float): initial guess for flow depth (m)
        Q (float): discharge (m^3/s)
        b (float): channel bottom width (m)
        n (float): Manning roughness coefficient
        S0 (float): channel bed slope
        z0 (float): elevation of the upstream end of the channel (m)

    Returns:
        (tuple): tuple containing:
            - y (float): water surface elevation (m)
            - d (float): flow depth (m)
    """

    # Initial parameters
    g = GRAVITY_G
    R = (b / 2) / d0
    V = Q / (b * d0)
    E = (V ** 2) / (2 * g) + z0

    # Iterative calculation
    while True:
        d = d0
        R = (b / 2) / d
        A = b * d
        P = b + 2 * d * math.sqrt(1 + R ** 2)
        S = (Q / (A * math.sqrt(S0))) ** (3 / 5) / (n ** 2)
        dE_dx = -S + (S / R ** (4 / 3)) * V ** 3 / (2 * g)
        dy = dE_dx * dx
        y = z0 + E - dy
        d = (-V ** 2 + math.sqrt(V ** 4 + 4 * g * S * A * dy)) / (2 * g * S)
        if abs(d - d0) < 0.001:
            break
        d0 = d

    return y, d
