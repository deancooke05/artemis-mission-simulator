import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Constants
# -----------------------------
G = 6.67430e-11
M_E = 5.972e24
R_E = 6.371e6
MU = G * M_E

MOON_DISTANCE = 384.4e6
MOON_PERIOD = 27.321661 * 24 * 3600
OMEGA_MOON = 2 * np.pi / MOON_PERIOD

LUNAR_RADIUS = 1737e3
TARGET_LUNAR_ALTITUDE = 3000e3
TARGET_LUNAR_ORBIT_RADIUS = LUNAR_RADIUS + TARGET_LUNAR_ALTITUDE
# -----------------------------
# Initial Earth orbit
# -----------------------------
altitude = 200e3
r0 = R_E + altitude
x0 = r0
y0 = 0.0

v_circular = np.sqrt(MU / r0)
vx0 = 0.0
vy0 = v_circular

# -----------------------------
# Departure settings
# -----------------------------
burn_time = 3000.0
delta_v = 3370.0

# -----------------------------
# Moon phase sweep
# -----------------------------
phase_values = np.linspace(5.82, 5.96, 15)

# -----------------------------
# Simulation settings
# -----------------------------
dt = 10.0
t_max = 500000
times = np.arange(0, t_max + dt, dt)

def derivatives(state):
    x, y, vx, vy = state
    r = np.sqrt(x**2 + y**2)
    ax = -MU * x / r**3
    ay = -MU * y / r**3
    return np.array([vx, vy, ax, ay], dtype=float)

def rk4(state, dt):
    k1 = derivatives(state)
    k2 = derivatives(state + 0.5 * dt * k1)
    k3 = derivatives(state + 0.5 * dt * k2)
    k4 = derivatives(state + dt * k3)
    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def prograde_burn(state, dv):
    x, y, vx, vy = state
    v = np.sqrt(vx**2 + vy**2)
    return np.array([
        x,
        y,
        vx + dv * vx / v,
        vy + dv * vy / v
    ], dtype=float)

def moon_position(t, phase0):
    theta = OMEGA_MOON * t + phase0
    return MOON_DISTANCE * np.cos(theta), MOON_DISTANCE * np.sin(theta)

results = []

print("Moon phase sweep results:\n")

for moon_phase_0 in phase_values:
    state = np.array([x0, y0, vx0, vy0], dtype=float)
    burn_done = False

    min_distance_to_moon = float("inf")
    best_encounter_error = float("inf")
    best_time = None

    for t in times:
        x, y, vx, vy = state
        moon_x, moon_y = moon_position(t, moon_phase_0)

        distance_to_moon = np.sqrt((x - moon_x)**2 + (y - moon_y)**2)
        encounter_error = abs(distance_to_moon - TARGET_LUNAR_ORBIT_RADIUS)

        if distance_to_moon < min_distance_to_moon:
            min_distance_to_moon = distance_to_moon

        if encounter_error < best_encounter_error:
            best_encounter_error = encounter_error
            best_time = t

        if (not burn_done) and (t >= burn_time):
            state = prograde_burn(state, delta_v)
            burn_done = True

        state = rk4(state, dt)

    results.append((moon_phase_0, min_distance_to_moon, best_encounter_error, best_time))

    print(
        f"Phase: {moon_phase_0:.3f} rad | "
        f"Closest center distance: {min_distance_to_moon/1e3:.1f} km | "
        f"Encounter error: {best_encounter_error/1e3:.1f} km | "
        f"Best time: {best_time/3600:.2f} h"
    )

best_result = min(results, key=lambda x: x[2])

print("\nBest phase result:")
print(
    f"Phase: {best_result[0]:.3f} rad | "
    f"Closest center distance: {best_result[1]/1e3:.1f} km | "
    f"Encounter error: {best_result[2]/1e3:.1f} km | "
    f"Best time: {best_result[3]/3600:.2f} h"
)