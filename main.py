import numpy as np

from simulation import run_simulation
from plotting import (
    plot_altitude,
    plot_velocity,
    plot_acceleration,
    plot_mass,
    plot_drag,
    plot_dynamic_pressure,
)


def main():
    results = run_simulation()

    times = results["times"]
    altitudes = results["altitudes"]
    velocities = results["velocities"]
    accelerations = results["accelerations"]
    masses = results["masses"]
    drags = results["drags"]
    dynamic_pressures = results["dynamic_pressures"]

    burnout_index = results["burnout_index"]
    max_q_index = results["max_q_index"]
    max_drag_index = results["max_drag_index"]

    print(f"Burnout altitude: {altitudes[burnout_index]:.2f} m")
    print(f"Burnout velocity: {velocities[burnout_index]:.2f} m/s")
    print(f"Maximum altitude: {np.max(altitudes):.2f} m")
    print(f"Maximum velocity: {np.max(velocities):.2f} m/s")
    print(f"Maximum acceleration: {np.max(accelerations):.2f} m/s²")
    print(f"Maximum drag: {drags[max_drag_index]:.2f} N at t = {times[max_drag_index]:.2f} s")
    print(f"Maximum dynamic pressure: {dynamic_pressures[max_q_index]:.2f} Pa at t = {times[max_q_index]:.2f} s")
    print(f"Altitude at Max Q: {altitudes[max_q_index]:.2f} m")
    print(f"Velocity at Max Q: {velocities[max_q_index]:.2f} m/s")

    plot_altitude(times, altitudes, burnout_index)
    plot_velocity(times, velocities, burnout_index)
    plot_acceleration(times, accelerations, burnout_index)
    plot_mass(times, masses, burnout_index)
    plot_drag(times, drags, max_drag_index)
    plot_dynamic_pressure(times, dynamic_pressures, max_q_index)


if __name__ == "__main__":
    main()
