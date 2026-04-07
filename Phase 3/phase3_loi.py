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

loi_delta_v = 1700.0
loi_trigger_distance = 9475e3

dt = 10.0
t_max = 500000
times = np.arange(0, t_max + dt, dt)

def moon_position(t, phase0):
    theta = OMEGA_MOON * t + phase0
    x_m = MOON_DISTANCE * np.cos(theta)
    y_m = MOON_DISTANCE * np.sin(theta)
    return x_m, y_m

def moon_velocity(t, phase0):
    theta = OMEGA_MOON * t + phase0
    vx_m = -MOON_DISTANCE * OMEGA_MOON * np.sin(theta)
    vy_m =  MOON_DISTANCE * OMEGA_MOON * np.cos(theta)
    return vx_m, vy_m

def derivatives(state, t):
    x, y, vx, vy = state

    # Earth gravity
    r_e = np.sqrt(x**2 + y**2)
    ax_e = -MU_E * x / r_e**3
    ay_e = -MU_E * y / r_e**3

    # Moon gravity
    x_m, y_m = moon_position(t, moon_phase_0)
    dx_m = x - x_m
    dy_m = y - y_m
    r_m = np.sqrt(dx_m**2 + dy_m**2)

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

def apply_loi_burn(state, t, dv):
    """
    Apply retrograde burn relative to Moon motion.
    """
    x, y, vx, vy = state
    vx_m, vy_m = moon_velocity(t, moon_phase_0)

    vx_rel = vx - vx_m
    vy_rel = vy - vy_m
    v_rel = np.sqrt(vx_rel**2 + vy_rel**2)

    ux = vx_rel / v_rel
    uy = vy_rel / v_rel

    vx_new = vx - dv * ux
    vy_new = vy - dv * uy

    return np.array([x, y, vx_new, vy_new], dtype=float)

state = np.array([x0, y0, vx0, vy0], dtype=float)

# Storage
xs = []
ys = []
moon_xs = []
moon_ys = []

moon_relative_distances = []
moon_relative_speeds = []
moon_relative_energies = []

burn_done = False
loi_done = False
loi_index = None
loi_time = None

min_distance_to_moon = float("inf")
best_encounter_error = float("inf")
best_time = None
best_sc_pos = None
best_moon_pos = None
best_center_distance = None

impact_occurred = False
impact_time = None
impact_distance = None

for i, t in enumerate(times):
    x, y, vx, vy = state

    moon_x, moon_y = moon_position(t, moon_phase_0)
    distance_to_moon = np.sqrt((x - moon_x)**2 + (y - moon_y)**2)
    encounter_error = abs(distance_to_moon - TARGET_LUNAR_ORBIT_RADIUS)

    moon_vx, moon_vy = moon_velocity(t, moon_phase_0)
    vx_rel = vx - moon_vx
    vy_rel = vy - moon_vy
    v_rel = np.sqrt(vx_rel**2 + vy_rel**2)
    moon_relative_energy = 0.5 * v_rel**2 - MU_M / distance_to_moon

    moon_relative_distances.append(distance_to_moon)
    moon_relative_speeds.append(v_rel)
    moon_relative_energies.append(moon_relative_energy)

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

    if distance_to_moon <= R_M:
        impact_occurred = True
        impact_time = t
        impact_distance = distance_to_moon
        break

    if (not burn_done) and (t >= burn_time):
        state = prograde_burn(state, delta_v)
        burn_done = True

    if burn_done and (not loi_done):
        if distance_to_moon <= loi_trigger_distance:
            state = apply_loi_burn(state, t, loi_delta_v)
            loi_done = True
            loi_index = i
            loi_time = t

    state = rk4_step(state, t, dt)

xs = np.array(xs)
ys = np.array(ys)
moon_xs = np.array(moon_xs)
moon_ys = np.array(moon_ys)
moon_relative_distances = np.array(moon_relative_distances)
moon_relative_speeds = np.array(moon_relative_speeds)
moon_relative_energies = np.array(moon_relative_energies)

final_x, final_y, final_vx, final_vy = state
final_mx, final_my = moon_position(t, moon_phase_0)
final_mvx, final_mvy = moon_velocity(t, moon_phase_0)

dx = final_x - final_mx
dy = final_y - final_my
r_rel = np.sqrt(dx**2 + dy**2)

vx_rel = final_vx - final_mvx
vy_rel = final_vy - final_mvy
v_rel = np.sqrt(vx_rel**2 + vy_rel**2)

specific_energy_moon = 0.5 * v_rel**2 - MU_M / r_rel

print(f"Circular velocity: {v_circular:.2f} m/s")
print(f"Burn time: {burn_time:.2f} s")
print(f"Translunar delta-v: {delta_v:.2f} m/s")
print(f"Moon initial phase angle: {moon_phase_0:.3f} rad")
print(f"LOI delta-v: {loi_delta_v:.2f} m/s")
print(f"Closest distance to Moon center: {min_distance_to_moon/1e3:.2f} km")
print(f"Best encounter distance to Moon center: {best_center_distance/1e3:.2f} km")
print(f"Target lunar orbit radius: {TARGET_LUNAR_ORBIT_RADIUS/1e3:.2f} km")
print(f"Encounter error: {best_encounter_error/1e3:.2f} km")
print(f"Best encounter time: {best_time/3600:.2f} hours")

if loi_done:
    print("LOI burn applied.")
    print(f"LOI time: {loi_time/3600:.2f} hours")
else:
    print("LOI burn not applied.")

if impact_occurred:
    print("Lunar impact detected.")
    print(f"Impact time: {impact_time/3600:.2f} hours")
    print(f"Impact distance to Moon center: {impact_distance/1e3:.2f} km")
else:
    print("No lunar impact detected.")

print(f"Final Moon-relative specific energy: {specific_energy_moon:.2f} J/kg")
if specific_energy_moon < 0:
    print("Spacecraft is bound to the Moon (captured).")
else:
    print("Spacecraft is not bound to the Moon.")

plt.figure(figsize=(9, 9))
plt.plot(xs, ys, label="Spacecraft Trajectory")

theta = np.linspace(0, 2*np.pi, 400)

earth_x = R_E * np.cos(theta)
earth_y = R_E * np.sin(theta)
plt.plot(earth_x, earth_y, label="Earth")

moon_orbit_x = MOON_DISTANCE * np.cos(theta)
moon_orbit_y = MOON_DISTANCE * np.sin(theta)
plt.plot(moon_orbit_x, moon_orbit_y, linestyle="--", label="Moon Orbit")

plt.plot(moon_xs, moon_ys, label="Moon Motion")

if best_moon_pos is not None:
    moon_target_x = best_moon_pos[0] + TARGET_LUNAR_ORBIT_RADIUS * np.cos(theta)
    moon_target_y = best_moon_pos[1] + TARGET_LUNAR_ORBIT_RADIUS * np.sin(theta)
    plt.plot(moon_target_x, moon_target_y, label="Target Lunar Orbit Radius")

if best_sc_pos is not None and best_moon_pos is not None:
    plt.scatter(best_sc_pos[0], best_sc_pos[1], label="Best Encounter")
    plt.scatter(best_moon_pos[0], best_moon_pos[1], label="Moon at Encounter")

if loi_done and loi_index is not None:
    plt.scatter(xs[loi_index], ys[loi_index], label="LOI Burn")

plt.gca().set_aspect("equal")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Translunar Transfer with Lunar Orbit Insertion")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(times[:len(moon_relative_distances)] / 3600, moon_relative_distances / 1e3, label="Distance to Moon Center")
plt.axhline(R_M / 1e3, linestyle="--", label="Moon Radius")
plt.axhline(TARGET_LUNAR_ORBIT_RADIUS / 1e3, linestyle="--", label="Target Orbit Radius")

if loi_done and loi_time is not None:
    plt.axvline(loi_time / 3600, linestyle="--", label="LOI Burn")

plt.xlabel("Time (hours)")
plt.ylabel("Distance (km)")
plt.title("Moon-Relative Distance vs Time")
plt.grid(True)
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(times[:len(moon_relative_speeds)] / 3600, moon_relative_speeds, label="Moon-Relative Speed")

if loi_done and loi_time is not None:
    plt.axvline(loi_time / 3600, linestyle="--", label="LOI Burn")

plt.xlabel("Time (hours)")
plt.ylabel("Speed (m/s)")
plt.title("Moon-Relative Speed vs Time")
plt.grid(True)
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(times[:len(moon_relative_energies)] / 3600, moon_relative_energies, label="Moon-Relative Specific Energy")
plt.axhline(0, linestyle="--", label="Bound/Unbound Boundary")

if loi_done and loi_time is not None:
    plt.axvline(loi_time / 3600, linestyle="--", label="LOI Burn")

plt.xlabel("Time (hours)")
plt.ylabel("Specific Energy (J/kg)")
plt.title("Moon-Relative Specific Energy vs Time")
plt.grid(True)
plt.legend()
plt.show()