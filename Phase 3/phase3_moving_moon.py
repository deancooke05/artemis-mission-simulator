import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Constants
# -----------------------------
G = 6.67430e-11
M_E = 5.972e24
R_E = 6.371e6
MU = G * M_E

MOON_DISTANCE = 384.4e6                 # m
MOON_PERIOD = 27.321661 * 24 * 3600     # s
OMEGA_MOON = 2 * np.pi / MOON_PERIOD

LUNAR_RADIUS = 1737e3                   # m
TARGET_LUNAR_ALTITUDE = 100e3           # m
TARGET_LUNAR_ORBIT_RADIUS = LUNAR_RADIUS + TARGET_LUNAR_ALTITUDE

altitude = 200e3
r0 = R_E + altitude
x0 = r0
y0 = 0.0

v_circular = np.sqrt(MU / r0)
vx0 = 0.0
vy0 = v_circular

burn_time = 3000.0
delta_v = 3370.0

# Moon initial phase angle
# Start with Moon on +x axis
moon_phase_0 = 0.0

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
        best_sc_pos = (x, y)
        best_moon_pos = (moon_x, moon_y)
        best_center_distance = distance_to_moon

    xs.append(x)
    ys.append(y)
    moon_xs.append(moon_x)
    moon_ys.append(moon_y)

    if (not burn_done) and (t >= burn_time):
        state = prograde_burn(state, delta_v)
        burn_done = True

    state = rk4(state, dt)

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

# Moon path over simulation
plt.plot(moon_xs, moon_ys, label="Moon Motion")

# markers
if best_sc_pos is not None and best_moon_pos is not None:
    plt.scatter(best_sc_pos[0], best_sc_pos[1], label="Best SC Encounter")
    plt.scatter(best_moon_pos[0], best_moon_pos[1], label="Moon at Encounter")

plt.gca().set_aspect("equal")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Earth Departure with Moving Moon Target")
plt.legend()
plt.grid(True)
plt.show()