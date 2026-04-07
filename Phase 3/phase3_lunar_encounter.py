import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11
M_E = 5.972e24
R_E = 6.371e6
MU = G * M_E

MOON_DISTANCE = 384.4e6          # m
MOON_X = MOON_DISTANCE
MOON_Y = 0.0

LUNAR_RADIUS = 1737e3            # m
TARGET_LUNAR_ALTITUDE = 100e3    # m
TARGET_LUNAR_ORBIT_RADIUS = LUNAR_RADIUS + TARGET_LUNAR_ALTITUDE

# Initial Earth orbit
altitude = 200e3
r0 = R_E + altitude
x0 = r0
y0 = 0.0

v_circular = np.sqrt(MU / r0)
vx0 = 0.0
vy0 = v_circular

# Sweep settings
burn_times = [2900, 2950, 3000, 3050, 3100]
delta_v_values = [3350.0, 3360.0, 3370.0, 3374.2, 3380.0]

# Simulation settings
dt = 5.0
t_max = 300000
times = np.arange(0, t_max, dt)

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

best_result = None
results = []

for burn_time in burn_times:
    for delta_v in delta_v_values:
        state = np.array([x0, y0, vx0, vy0], dtype=float)

        burn_done = False
        min_distance_to_moon = float("inf")
        best_encounter_error = float("inf")
        best_distance_at_encounter = None

        for t in times:
            x, y, vx, vy = state

            distance_to_moon = np.sqrt((x - MOON_X)**2 + (y - MOON_Y)**2)

            if distance_to_moon < min_distance_to_moon:
                min_distance_to_moon = distance_to_moon

            encounter_error = abs(distance_to_moon - TARGET_LUNAR_ORBIT_RADIUS)

            if encounter_error < best_encounter_error:
                best_encounter_error = encounter_error
                best_distance_at_encounter = distance_to_moon

            if (not burn_done) and (t >= burn_time):
                state = prograde_burn(state, delta_v)
                burn_done = True

            state = rk4(state, dt)

        result = {
            "burn_time": burn_time,
            "delta_v": delta_v,
            "closest_to_center": min_distance_to_moon,
            "best_encounter_error": best_encounter_error,
            "distance_at_best_encounter": best_distance_at_encounter,
        }
        results.append(result)

        if best_result is None or best_encounter_error < best_result["best_encounter_error"]:
            best_result = result

print("Lunar encounter sweep results:\n")
for r in results:
    print(
        f"Burn time: {r['burn_time']:.0f} s | "
        f"Delta-v: {r['delta_v']:.1f} m/s | "
        f"Closest to Moon center: {r['closest_to_center']/1e6:.3f} Mm | "
        f"Encounter error vs target orbit radius: {r['best_encounter_error']/1e3:.1f} km"
    )

print("\nBest result:")
print(
    f"Burn time: {best_result['burn_time']:.0f} s | "
    f"Delta-v: {best_result['delta_v']:.1f} m/s | "
    f"Closest to Moon center: {best_result['closest_to_center']/1e3:.1f} km | "
    f"Target lunar orbit radius: {TARGET_LUNAR_ORBIT_RADIUS/1e3:.1f} km | "
    f"Encounter error: {best_result['best_encounter_error']/1e3:.1f} km"
)