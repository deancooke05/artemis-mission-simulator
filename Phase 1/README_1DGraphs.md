These values are physically plausible for a first-order ascent model, but not intended to replicate the true Artemis II ascent profile exactly



A one-dimensional vertical ascent model was developed to simulate the early launch phase of a heavy-lift launch vehicle. The model includes time-varying mass due to propellant consumption, constant thrust during powered ascent, aerodynamic drag using an exponential atmosphere model, and gravitational weight. Numerical integration was performed using a forward Euler method to estimate altitude, velocity, and acceleration as functions of time.



The simulation produced a burnout altitude of 85.3 km and a burnout velocity of 1629 m/s, indicating that the launch vehicle exits the densest part of the atmosphere before engine cutoff. The maximum altitude reached was 154.6 km, demonstrating the contribution of the post-burn coasting phase. The maximum acceleration of 25.2 m/s², equivalent to approximately 2.6 g, is within a physically plausible range for a simplified crewed heavy-lift ascent model.



Introducing altitude-dependent gravity produced a small but physically meaningful increase in burnout altitude, burnout velocity, maximum altitude, and maximum acceleration. This is expected because gravitational acceleration decreases slightly with altitude, reducing the vehicle weight during ascent and increasing the net upward force. The modest scale of the change suggests that the updated model behaves realistically and remains numerically stable



now we've got to calculate dynamic pressure. even if thrust is high, the rocket cant just brute-force everything because aerodynamic loads matter.

Max Q is basically:

* where the vehicle is going fast enough
* while the air is still dense enough
* that aerodynamic stress peaks



The simulation predicts a maximum dynamic pressure of 24.2 kPa at 65.7 s into flight, occurring at an altitude of 10.7 km and a velocity of 372 m/s. This is consistent with the expected Max Q event during ascent, where increasing velocity and decreasing atmospheric density combine to produce peak aerodynamic loading. The corresponding maximum drag force is approximately 0.97 MN. Because drag in the model is directly proportional to dynamic pressure, both quantities peak at the same point in time.



The results indicate that aerodynamic effects are most significant during the lower-to-mid atmosphere portion of the ascent, while later flight is dominated more strongly by gravitational and inertial effects as atmospheric density decreases.



Key Findings

Ascent Performance

Burnout altitude ≈ 85 km

Burnout velocity ≈ 1.63 km/s

Maximum altitude ≈ 155 km



Interpretation:

The vehicle exits the dense atmosphere during powered ascent and continues to climb significantly during the coasting phase due to inertia.



Acceleration Behaviour

Maximum acceleration ≈ 25 m/s² (\~2.6 g)



Interpretation:

Acceleration increases during the burn due to decreasing mass, demonstrating the direct effect of propellant consumption on vehicle dynamics.



Atmospheric Effects \& Max Q

Max dynamic pressure ≈ 24 kPa

Occurs at:

\~65.7 s

\~10.7 km altitude

\~372 m/s velocity



Interpretation:

Max Q occurs in the lower atmosphere where the balance between increasing velocity and decreasing air density produces peak aerodynamic loading.



Drag Behaviour

Maximum drag ≈ 0.97 MN

Occurs at same time as Max Q



Interpretation:

Since drag is proportional to dynamic pressure, both peak simultaneously, confirming internal consistency of the model.



Limitations

1D vertical motion (no gravity turn)

No staging (real rockets stage)

Constant thrust assumption

Constant drag coefficient (ignores Mach effects)

Simplified exponential atmosphere

Euler integration (low accuracy vs RK4)



The model is intended as a first-order approximation and does not aim to replicate the full Artemis II ascent profile



Development Challenges

🐍 Python Environment Issues

Multiple Python installs caused missing package errors

Resolved using virtual environments

📦 Module Import Errors

Incorrect module naming (environment.py vs atmosphere.py)

Python cache (\_\_pycache\_\_) caused stale imports

📊 Plotting Errors

Incorrect function definitions in plotting.py

Resolved by restructuring plotting module



Significant debugging effort was required to resolve Python environment conflicts and module import issues, reflecting real-world software engineering challenges



Aerospace Simulation Project

Developed a Python-based simulation of a launch vehicle ascent inspired by Artemis II

Modelled variable mass propulsion, atmospheric drag, and altitude-dependent gravity

Implemented dynamic pressure calculations to identify Max Q conditions

Built modular code architecture separating physics, simulation, and visualisation

Analysed ascent performance including burnout conditions and aerodynamic loads



\## Overview

\## Features

\## Physics Model

\## Results

\## Limitations

\## Future Work

\## How to Run

