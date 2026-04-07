import numpy as np
import matplotlib.pyplot as plt

G = 6.67430e-11

# Earth
M_E = 5.972e24
R_E = 6.371e6
MU_E = G * M_E

# Moon
M_M = 7.34767309e22
R_M = 1737e3
MU_M = G * M_M

# Moon orbit
MOON_DISTANCE = 384.4e6
MOON_PERIOD = 27.321661 * 24 * 3600
OMEGA_MOON = 2 * np.pi / MOON_PERIOD

# Target lunar orbit radius
TARGET_LUNAR_ALTITUDE = 3000e3
TARGET_LUNAR_ORBIT_RADIUS = R_M + TARGET_LUNAR_ALTITUDE

altitude = 200e3
r0 = R_E + altitude
x0 = r0
y0 = 0.0

v_circular = np.sqrt(MU_E / r0)
vx0 = 0.0
vy0 = v_circular

burn_time = 3000.0
delta_v = 3370.0
moon_phase_0 = 5.910

dt = 10.0
t_max = 500000
times = np.arange(0, t_max + dt, dt)

def moon_position(t, phase0):
    theta = OMEGA_MOON * t + phase0
    x_m = MOON_DISTANCE * np.cos(theta)
    y_m = MOON_DISTANCE * np.sin(theta)
    return x_m, y_m

def derivatives(state, t):
    x, y, vx, vy = state

    # Earth-relative distance
    r_e = np.sqrt(x**2 + y**2)

    # Earth gravity
    ax_e = -MU_E * x / r_e**3
    ay_e = -MU_E * y / r_e**3

    # Moon position
    x_m, y_m = moon_position(t, moon_phase_0)

    # Spacecraft relative to Moon
    dx_m = x - x_m
    dy_m = y - y_m
    r_m = np.sqrt(dx_m**2 + dy_m**2)

    # Moon gravity
    ax_m = -MU_M * dx_m / r_m**3
    ay_m = -MU_M * dy_m / r_m**3

    ax = ax_e + ax_m
    ay = ay_e + ay_m

    return np.array([vx, vy, ax, ay], dtype=float)

def rk4_step(state, t, dt):
    k1 = derivatives(state, t)
    k2 = derivatives(state + 0.5 * dt * k1, t + 0.5 * dt)
    k3 = derivatives(state + 0.5 * dt * k2, t + 0.5 * dt)
    k4 = derivatives(state + dt * k3, t + dt)
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

state = np.array([x0, y0, vx0, vy0], dtype=float)

xs = []
ys = []
moon_xs = []
moon_ys = []

burn_done = False

min_distance_to_moon = float("inf")
best_encounter_error = float("inf")
best_time = None
best_sc_pos = None
best_moon_pos = None
best_center_distance = None

impact_occurred = False
impact_time = None
impact_sc_pos = None
impact_moon_pos = None
impact_distance = None

for t in times:
    x, y, vx, vy = state

    moon_x, moon_y = moon_position(t, moon_phase_0)
    distance_to_moon = np.sqrt((x - moon_x)**2 + (y - moon_y)**2)
    encounter_error = abs(distance_to_moon - TARGET_LUNAR_ORBIT_RADIUS)

    # Record minimum distance and best target-shell encounter
    if distance_to_moon < min_distance_to_moon:
        min_distance_to_moon = distance_to_moon

    if encounter_error < best_encounter_error:
        best_encounter_error = encounter_error
        best_time = t
        best_sc_pos = (x, y)
        best_moon_pos = (moon_x, moon_y)
        best_center_distance = distance_to_moon

    xs.append(x)
    ys.append(y)
    moon_xs.append(moon_x)
    moon_ys.append(moon_y)

    # Check for lunar impact
    if distance_to_moon <= R_M:
        impact_occurred = True
        impact_time = t
        impact_sc_pos = (x, y)
        impact_moon_pos = (moon_x, moon_y)
        impact_distance = distance_to_moon
        break

    # Departure burn
    if (not burn_done) and (t >= burn_time):
        state = prograde_burn(state, delta_v)
        burn_done = True

    state = rk4_step(state, t, dt)

xs = np.array(xs)
ys = np.array(ys)
moon_xs = np.array(moon_xs)
moon_ys = np.array(moon_ys)

print(f"Circular velocity: {v_circular:.2f} m/s")
print(f"Burn time: {burn_time:.2f} s")
print(f"Delta-v: {delta_v:.2f} m/s")
print(f"Moon initial phase angle: {moon_phase_0:.3f} rad")
print(f"Closest distance to Moon center: {min_distance_to_moon/1e3:.2f} km")
print(f"Best encounter distance to Moon center: {best_center_distance/1e3:.2f} km")
print(f"Target lunar orbit radius: {TARGET_LUNAR_ORBIT_RADIUS/1e3:.2f} km")
print(f"Encounter error: {best_encounter_error/1e3:.2f} km")
print(f"Best encounter time: {best_time/3600:.2f} hours")

if impact_occurred:
    print("Lunar impact detected.")
    print(f"Impact time: {impact_time/3600:.2f} hours")
    print(f"Impact distance to Moon center: {impact_distance/1e3:.2f} km")
else:
    print("No lunar impact detected.")

plt.figure(figsize=(9, 9))
plt.plot(xs, ys, label="Spacecraft Trajectory")

# Earth
theta = np.linspace(0, 2*np.pi, 400)
earth_x = R_E * np.cos(theta)
earth_y = R_E * np.sin(theta)
plt.plot(earth_x, earth_y, label="Earth")

# Moon orbit
moon_orbit_x = MOON_DISTANCE * np.cos(theta)
moon_orbit_y = MOON_DISTANCE * np.sin(theta)
plt.plot(moon_orbit_x, moon_orbit_y, linestyle="--", label="Moon Orbit")

# Moon motion during sim
plt.plot(moon_xs, moon_ys, label="Moon Motion")

# Moon body at best encounter time
if best_moon_pos is not None:
    moon_body_x = best_moon_pos[0] + R_M * np.cos(theta)
    moon_body_y = best_moon_pos[1] + R_M * np.sin(theta)
    plt.plot(moon_body_x, moon_body_y, label="Moon at Best Encounter")

if best_sc_pos is not None and best_moon_pos is not None:
    plt.scatter(best_sc_pos[0], best_sc_pos[1], label="Best SC Encounter")
    plt.scatter(best_moon_pos[0], best_moon_pos[1], label="Moon Center at Encounter")

if impact_occurred and impact_sc_pos is not None:
    plt.scatter(impact_sc_pos[0], impact_sc_pos[1], label="Impact Point")

plt.gca().set_aspect("equal")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Earth Departure with Moving Moon, Lunar Gravity, and Impact Detection")
plt.legend()
plt.grid(True)
plt.show()