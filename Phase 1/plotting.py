import matplotlib.pyplot as plt


def plot_altitude(times, altitudes, burnout_index):
    plt.figure(figsize=(10, 6))
    plt.plot(times, altitudes, label="Altitude")
    plt.scatter(times[burnout_index], altitudes[burnout_index], label="Burnout")
    plt.xlabel("Time (s)")
    plt.ylabel("Altitude (m)")
    plt.title("Altitude vs Time")
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_velocity(times, velocities, burnout_index):
    plt.figure(figsize=(10, 6))
    plt.plot(times, velocities, label="Velocity")
    plt.scatter(times[burnout_index], velocities[burnout_index], label="Burnout")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Velocity vs Time")
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_acceleration(times, accelerations, burnout_index):
    plt.figure(figsize=(10, 6))
    plt.plot(times, accelerations, label="Acceleration")
    plt.scatter(times[burnout_index], accelerations[burnout_index], label="Burnout")
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (m/s²)")
    plt.title("Acceleration vs Time")
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_mass(times, masses, burnout_index):
    plt.figure(figsize=(10, 6))
    plt.plot(times, masses, label="Mass")
    plt.scatter(times[burnout_index], masses[burnout_index], label="Burnout")
    plt.xlabel("Time (s)")
    plt.ylabel("Mass (kg)")
    plt.title("Mass vs Time")
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_drag(times, drags, max_drag_index):
    plt.figure(figsize=(10, 6))
    plt.plot(times, drags, label="Drag")
    plt.scatter(times[max_drag_index], drags[max_drag_index], label="Max Drag")
    plt.xlabel("Time (s)")
    plt.ylabel("Drag Force (N)")
    plt.title("Drag vs Time")
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_dynamic_pressure(times, dynamic_pressures, max_q_index):
    plt.figure(figsize=(10, 6))
    plt.plot(times, dynamic_pressures, label="Dynamic Pressure")
    plt.scatter(times[max_q_index], dynamic_pressures[max_q_index], label="Max Q")
    plt.xlabel("Time (s)")
    plt.ylabel("Dynamic Pressure (Pa)")
    plt.title("Dynamic Pressure vs Time")
    plt.grid(True)
    plt.legend()
    plt.show()