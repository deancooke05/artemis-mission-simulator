import numpy as np

from rocket import get_mass, get_thrust, CD, AREA, BURN_TIME
from atmosphere import air_density, gravity, dynamic_pressure


def run_simulation(dt=0.1, t_max=200.0):
    """Run the 1D vertical ascent simulation."""

    times = np.arange(0, t_max + dt, dt)

    altitudes = np.zeros_like(times)
    velocities = np.zeros_like(times)
    accelerations = np.zeros_like(times)
    masses = np.zeros_like(times)
    drags = np.zeros_like(times)
    dynamic_pressures = np.zeros_like(times)
    densities = np.zeros_like(times)

    for i in range(1, len(times)):
        t = times[i - 1]
        altitude = altitudes[i - 1]
        velocity = velocities[i - 1]

        mass = get_mass(t)
        thrust = get_thrust(t)

        rho = air_density(altitude)
        q = dynamic_pressure(altitude, velocity)
        drag = q * CD * AREA

        if velocity < 0:
            drag_force = drag
        else:
            drag_force = -drag

        g = gravity(altitude)
        weight = mass * g
        net_force = thrust + drag_force - weight
        acceleration = net_force / mass

        new_velocity = velocity + acceleration * dt
        new_altitude = altitude + new_velocity * dt

        if new_altitude < 0:
            new_altitude = 0
            new_velocity = 0

        altitudes[i] = new_altitude
        velocities[i] = new_velocity
        accelerations[i] = acceleration
        masses[i] = mass
        drags[i] = drag
        dynamic_pressures[i] = q
        densities[i] = rho

    masses[0] = get_mass(0)

    burnout_index = np.argmin(np.abs(times - BURN_TIME))
    max_q_index = np.argmax(dynamic_pressures)
    max_drag_index = np.argmax(drags)

    return {
        "times": times,
        "altitudes": altitudes,
        "velocities": velocities,
        "accelerations": accelerations,
        "masses": masses,
        "drags": drags,
        "dynamic_pressures": dynamic_pressures,
        "densities": densities,
        "burnout_index": burnout_index,
        "max_q_index": max_q_index,
        "max_drag_index": max_drag_index,
    }