import numpy as np

# Rocket parameters
INITIAL_MASS = 2.6e6      # kg
DRY_MASS = 1.0e6          # kg
THRUST = 3.5e7            # N
BURN_TIME = 150.0         # s
CD = 0.5                  # drag coefficient
AREA = 80.0               # m^2

MASS_FLOW_RATE = (INITIAL_MASS - DRY_MASS) / BURN_TIME


def get_mass(t):
    """Return rocket mass at time t."""
    if t <= BURN_TIME:
        return INITIAL_MASS - MASS_FLOW_RATE * t
    return DRY_MASS


def get_thrust(t):
    """Return rocket thrust at time t."""
    return THRUST if t <= BURN_TIME else 0.0