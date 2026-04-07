import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11
M_E = 5.972e24
R_E = 6.371e6
MU = G * M_E

MOON_DISTANCE = 384.4e6   # m

# Initial orbit
altitude = 200e3
r0 = R_E + altitude

x0 = r0
y0 = 0.0

v_circular = np.sqrt(MU / r0)
v_escape = np.sqrt(2 * MU / r0)

vx0 = 0.0
vy0 = v_circular

# Burn
burn_time = 2000.0
delta_v = 3200.0

# Simulation
dt = 2.0
t_max = 120000
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

state = np.array([x0, y0, vx0, vy0], dtype=float)

xs = []
ys = []
radii = []

burn_done = False
burn_index = None

for i, t in enumerate(times):
    x, y, vx, vy = state
    r = np.sqrt(x**2 + y**2)

    xs.append(x)
    ys.append(y)
    radii.append(r)

    if (not burn_done) and (t >= burn_time):
        state = prograde_burn(state, delta_v)
        burn_done = True
        burn_index = i

    state = rk4(state, dt)

xs = np.array(xs)
ys = np.array(ys)
radii = np.array(radii)

reaches_moon_distance = np.max(radii) >= MOON_DISTANCE

print(f"Circular velocity: {v_circular:.2f} m/s")
print(f"Escape velocity: {v_escape:.2f} m/s")
print(f"Delta-v applied: {delta_v:.2f} m/s")
print(f"Max distance from Earth: {np.max(radii)/1e6:.2f} Mm")
print(f"Moon distance: {MOON_DISTANCE/1e6:.2f} Mm")
print(f"Reaches Moon distance: {reaches_moon_distance}")

plt.figure(figsize=(8, 8))
plt.plot(xs, ys, label="Trajectory")

theta = np.linspace(0, 2*np.pi, 400)

# Earth
earth_x = R_E * np.cos(theta)
earth_y = R_E * np.sin(theta)
plt.plot(earth_x, earth_y, label="Earth")

# Moon-distance reference circle
moon_x = MOON_DISTANCE * np.cos(theta)
moon_y = MOON_DISTANCE * np.sin(theta)
plt.plot(moon_x, moon_y, linestyle="--", label="Moon Distance")

if burn_index is not None:
    plt.scatter(xs[burn_index], ys[burn_index], label="Burn Point")

plt.gca().set_aspect("equal")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Earth Departure Trajectory with Moon-Distance Reference")
plt.legend()
plt.grid(True)
plt.show()