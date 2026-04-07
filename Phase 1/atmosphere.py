import numpy as np

G0 = 9.81          # m/s^2
RHO0 = 1.225       # kg/m^3
H_SCALE = 8500.0   # m
R_E = 6.371e6      # m


def air_density(altitude):
    return RHO0 * np.exp(-altitude / H_SCALE)


def gravity(altitude):
    return G0 * (R_E / (R_E + altitude))**2


def dynamic_pressure(altitude, velocity):
    rho = air_density(altitude)
    return 0.5 * rho * velocity**2