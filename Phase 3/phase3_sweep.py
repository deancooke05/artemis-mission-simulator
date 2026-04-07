import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11
M_E = 5.972e24
R_E = 6.371e6
MU = G * M_E
MOON_DISTANCE = 384.4e6  # m

# Initial orbit
altitude = 200e3
r0 = R_E + altitude
x0 = r0
y0 = 0.0

v_circular = np.sqrt(MU / r0)
v_escape = np.sqrt(2 * MU / r0)

vx0 = 0.0
vy0 = v_circular

# Burn timing
burn_time = 2000.0

# Simulation settings
dt = 5.0
t_max = 300000
times = np.arange(0, t_max, dt)

delta_v_values = [3200, 3250, 3300, 3350, 3400]

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

results = []

plt.figure(figsize=(8, 8))

theta = np.linspace(0, 2*np.pi, 400)
earth_x = R_E * np.cos(theta)
earth_y = R_E * np.sin(theta)
moon_x = MOON_DISTANCE * np.cos(theta)
moon_y = MOON_DISTANCE * np.sin(theta)

plt.plot(earth_x, earth_y, label="Earth")
plt.plot(moon_x, moon_y, linestyle="--", label="Moon Distance")

for delta_v in delta_v_values:
    state = np.array([x0, y0, vx0, vy0], dtype=float)

    xs = []
    ys = []
    radii = []

    burn_done = False

    for t in times:
        x, y, vx, vy = state
        r = np.sqrt(x**2 + y**2)

        xs.append(x)
        ys.append(y)
        radii.append(r)

        if (not burn_done) and (t >= burn_time):
            state = prograde_burn(state, delta_v)
            burn_done = True

        state = rk4(state, dt)

    xs = np.array(xs)
    ys = np.array(ys)
    radii = np.array(radii)

    max_distance = np.max(radii)
    reaches_moon = max_distance >= MOON_DISTANCE

    results.append((delta_v, max_distance, reaches_moon))
    plt.plot(xs, ys, label=f"{delta_v} m/s")

print(f"Circular velocity: {v_circular:.2f} m/s")
print(f"Escape velocity: {v_escape:.2f} m/s")
print()

for delta_v, max_distance, reaches_moon in results:
    print(
        f"Delta-v: {delta_v:.0f} m/s | "
        f"Max distance: {max_distance/1e6:.2f} Mm | "
        f"Reaches Moon distance: {reaches_moon}"
    )

plt.gca().set_aspect("equal")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Earth Departure Sensitivity to Delta-v")
plt.legend()
plt.grid(True)
plt.show()