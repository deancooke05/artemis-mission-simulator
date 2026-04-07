import numpy as np
import matplotlib.pyplot as plt

G = 6.67430e-11
M_E = 5.972e24
R_E = 6.371e6
MU = G * M_E

altitude0 = 200e3
r0 = R_E + altitude0

x0 = r0
y0 = 0.0

v_circular_0 = np.sqrt(MU / r0)
v_escape_0 = np.sqrt(2 * MU / r0)

vx0 = 0.0
vy0 = v_circular_0

burn1_time = 2000.0      # first burn time (s)
delta_v1 = 100.0         # first burn magnitude (m/s)

dt = 1.0
t_max = 14000
times = np.arange(0, t_max + dt, dt)

def derivatives(state):
    x, y, vx, vy = state
    r = np.sqrt(x**2 + y**2)

    ax = -MU * x / r**3
    ay = -MU * y / r**3

    return np.array([vx, vy, ax, ay], dtype=float)

def rk4_step(state, dt):
    k1 = derivatives(state)
    k2 = derivatives(state + 0.5 * dt * k1)
    k3 = derivatives(state + 0.5 * dt * k2)
    k4 = derivatives(state + dt * k3)
    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def apply_prograde_burn(state, delta_v):
    x, y, vx, vy = state
    v = np.sqrt(vx**2 + vy**2)

    vx_unit = vx / v
    vy_unit = vy / v

    vx_new = vx + delta_v * vx_unit
    vy_new = vy + delta_v * vy_unit

    return np.array([x, y, vx_new, vy_new], dtype=float)

state = np.array([x0, y0, vx0, vy0], dtype=float)

xs = []
ys = []
altitudes = []
speeds = []
energies = []

burn1_applied = False
burn2_applied = False

burn1_index = None
burn2_index = None
delta_v2 = None

previous_altitude = None
rising_after_burn1 = False

for i, t in enumerate(times):
    x, y, vx, vy = state

    r = np.sqrt(x**2 + y**2)
    v = np.sqrt(vx**2 + vy**2)
    altitude = r - R_E
    energy = 0.5 * v**2 - MU / r

    xs.append(x)
    ys.append(y)
    altitudes.append(altitude)
    speeds.append(v)
    energies.append(energy)

    # Burn 1: raise apoapsis
    if (not burn1_applied) and (t >= burn1_time):
        state = apply_prograde_burn(state, delta_v1)
        burn1_applied = True
        burn1_index = i
        rising_after_burn1 = True

    # Burn 2: circularise at apoapsis
    if burn1_applied and (not burn2_applied) and previous_altitude is not None:
        if rising_after_burn1 and altitude < previous_altitude:
            x_b, y_b, vx_b, vy_b = state
            r_b = np.sqrt(x_b**2 + y_b**2)
            v_b = np.sqrt(vx_b**2 + vy_b**2)

            v_circular_target = np.sqrt(MU / r_b)
            delta_v2 = v_circular_target - v_b

            state = apply_prograde_burn(state, delta_v2)
            burn2_applied = True
            burn2_index = i

    previous_altitude = altitude
    state = rk4_step(state, dt)

xs = np.array(xs)
ys = np.array(ys)
altitudes = np.array(altitudes)
speeds = np.array(speeds)
energies = np.array(energies)

print(f"Initial circular orbit velocity: {v_circular_0:.2f} m/s")
print(f"Escape velocity at initial orbit: {v_escape_0:.2f} m/s")
print(f"Burn 1 time: {burn1_time:.2f} s")
print(f"Burn 1 delta-v: {delta_v1:.2f} m/s")

if burn2_applied and delta_v2 is not None:
    print(f"Burn 2 delta-v: {delta_v2:.2f} m/s")
    print(f"Burn 2 time: {times[burn2_index]:.2f} s")
else:
    print("Burn 2 was not applied.")

print(f"Minimum altitude: {np.min(altitudes):.2f} m")
print(f"Maximum altitude: {np.max(altitudes):.2f} m")
print(f"Minimum speed: {np.min(speeds):.2f} m/s")
print(f"Maximum speed: {np.max(speeds):.2f} m/s")
print(f"Mean specific orbital energy: {np.mean(energies):.2f} J/kg")

plt.figure(figsize=(7, 7))
plt.plot(xs, ys, label="Trajectory")

theta = np.linspace(0, 2*np.pi, 300)
earth_x = R_E * np.cos(theta)
earth_y = R_E * np.sin(theta)
plt.plot(earth_x, earth_y, label="Earth")

if burn1_index is not None:
    plt.scatter(xs[burn1_index], ys[burn1_index], label="Burn 1")
if burn2_index is not None:
    plt.scatter(xs[burn2_index], ys[burn2_index], label="Burn 2")

plt.gca().set_aspect("equal")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Two-Burn Orbit Raise and Circularisation")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(times, altitudes, label="Altitude")
if burn1_index is not None:
    plt.axvline(times[burn1_index], linestyle="--", label="Burn 1")
if burn2_index is not None:
    plt.axvline(times[burn2_index], linestyle="--", label="Burn 2")
plt.xlabel("Time (s)")
plt.ylabel("Altitude (m)")
plt.title("Altitude vs Time")
plt.grid(True)
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(times, speeds, label="Speed")
if burn1_index is not None:
    plt.axvline(times[burn1_index], linestyle="--", label="Burn 1")
if burn2_index is not None:
    plt.axvline(times[burn2_index], linestyle="--", label="Burn 2")
plt.xlabel("Time (s)")
plt.ylabel("Speed (m/s)")
plt.title("Speed vs Time")
plt.grid(True)
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(times, energies, label="Specific Orbital Energy")
if burn1_index is not None:
    plt.axvline(times[burn1_index], linestyle="--", label="Burn 1")
if burn2_index is not None:
    plt.axvline(times[burn2_index], linestyle="--", label="Burn 2")
plt.xlabel("Time (s)")
plt.ylabel("Specific Orbital Energy (J/kg)")
plt.title("Specific Orbital Energy vs Time")
plt.grid(True)
plt.legend()
plt.show()