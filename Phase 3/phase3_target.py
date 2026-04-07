import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11
M_E = 5.972e24
R_E = 6.371e6
MU = G * M_E

MOON_DISTANCE = 384.4e6

# Moon position (fixed target)
moon_x = MOON_DISTANCE
moon_y = 0.0

# Initial orbit
altitude = 200e3
r0 = R_E + altitude

x0 = r0
y0 = 0.0

v_circular = np.sqrt(MU / r0)

vx0 = 0.0
vy0 = v_circular

# Burn settings
burn_time = 3000
delta_v_values = [3330, 3340, 3350, 3360, 3374.2]

# Simulation
dt = 5.0
t_max = 300000
times = np.arange(0, t_max, dt)

def derivatives(state):
    x, y, vx, vy = state
    r = np.sqrt(x**2 + y**2)

    ax = -MU * x / r**3
    ay = -MU * y / r**3

    return np.array([vx, vy, ax, ay])

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
    ])

plt.figure(figsize=(8, 8))

theta = np.linspace(0, 2*np.pi, 400)

# Earth
plt.plot(R_E*np.cos(theta), R_E*np.sin(theta), label="Earth")

# Moon orbit
plt.plot(
    MOON_DISTANCE*np.cos(theta),
    MOON_DISTANCE*np.sin(theta),
    linestyle="--",
    label="Moon Orbit"
)

# Moon position
plt.scatter(moon_x, moon_y, color="black", label="Moon Target")

print("Closest approach results:\n")

for delta_v in delta_v_values:
    state = np.array([x0, y0, vx0, vy0], dtype=float)

    xs = []
    ys = []
    min_distance_to_moon = float("inf")

    burn_done = False

    for t in times:
        x, y, vx, vy = state

        xs.append(x)
        ys.append(y)

        # Distance to Moon
        distance_to_moon = np.sqrt((x - moon_x)**2 + (y - moon_y)**2)

        if distance_to_moon < min_distance_to_moon:
            min_distance_to_moon = distance_to_moon

        if (not burn_done) and (t >= burn_time):
            state = prograde_burn(state, delta_v)
            burn_done = True

        state = rk4(state, dt)

    xs = np.array(xs)
    ys = np.array(ys)

    print(
        f"Delta-v: {delta_v} m/s | "
        f"Closest approach: {min_distance_to_moon/1e6:.2f} Mm"
    )

    plt.plot(xs, ys, label=f"{delta_v} m/s")

plt.gca().set_aspect("equal")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Earth Departure with Moon Target")
plt.legend()
plt.grid(True)
plt.show()