# artemis-mission-simulator
Python simulation of an Artemis-style Earth–Moon mission including ascent, orbital transfer, translunar injection, moving Moon targeting, and lunar orbit insertion.

# Artemis-Style Translunar Mission Simulator

## Overview

This project is a Python based simulation of an Artemis style Earth to Moon mission. It was developed to explore the orbital mechanics behind launch, Earth orbit, translunar injection, lunar targeting, and LOI.

The simulation begins with a simplified 1D launch and ascent model, including variable mass, thrust, drag, and gravity. It then expands into a 2D orbital mechanics program using integration to model circular and elliptical Earth orbits, delta-v manoeuvres, and orbit raising. The final phase extends the model to an Earth to Moon transfer scenario with a moving Moon, lunar gravity, and a retrograde lunar orbit insertion burn.

A major part of the project involved improving both the physics and the numerical methods used. Early orbital models were propagated using Euler integration, which revealed errors in stability and energy conservation. These issues were corrected by a ridiculous amount of research and switching to a 'fourth-order Runge–Kutta (RK4)' integrator. Additional work included tuning translunar injection conditions, solving lunar phase-targeting problems, and refining the lunar orbit insertion sequence to achieve a non-impacting captured lunar trajectory.

The final model demonstrates a successful simplified lunar capture case in which the spacecraft departs Earth orbit, reaches the Moon at the correct phase, avoids impact, and ends with negative Moon-relative specific orbital energy, indicating lunar capture.

This project was built as both a learning exercise and a portfolio demonstration of orbital mechanics, numerical simulation, and iterative aerospace problem-solving.

## Features

- 1D vertical ascent simulation with thrust, variable mass, atmospheric drag, and gravity
- 2D Earth orbit simulation using numerical integration
- Circular and elliptical orbit modelling
- Delta-v manoeuvre simulation
- Two-burn orbit raising and circularisation
- Translunar injection modelling
- Moving Moon targeting and phase-angle analysis
- Lunar gravity inclusion
- Lunar impact detection
- Lunar orbit insertion (LOI) modelling
- Moon-relative energy analysis for capture detection
- Visualisation of trajectory, distance, speed, and specific orbital energy

'''text
artemis-mission-simulator/
│
├── README.md
├── LICENSE
├── .gitignore
├── main.py
│
├── phase1/
│   ├── rocket.py
│   ├── atmosphere.py
│   ├── simulation.py
│   └── plotting.py
│
├── phase2/
│   ├── orbit_sim.py
│   └── orbit_transfer.py
│
├── phase3/
│   ├── phase3_escape.py
│   ├── phase3_phase_sweep.py
│   ├── phase3_moving_moon.py
│   ├── phase3_lunar_gravity.py
│   └── phase3_loi.py
│
└── results/
    ├── phase1/
    ├── phase2/
    └── phase3/

** Physics and Methods **

The simulation is based on Newtonian mechanics and numerical time integration.

For ascent, the model includes:

thrust
variable mass due to propellant burn
aerodynamic drag
gravity

For orbital motion, the project uses two-dimensional position and velocity vectors. Earth and Moon gravity are modelled using inverse-square gravitational acceleration.

The spacecraft state is propagated numerically. Forward Euler integration was implemented early in the project but produced noticeable numerical errors in orbital stability and energy conservation. This was replaced by a fourth-order Runge–Kutta (RK4) method, which significantly improved accuracy and stability.

Specific orbital energy is used as a key diagnostic quantity:

positive specific energy indicates an unbound trajectory
negative specific energy indicates a bound orbit

Lunar orbit insertion is modelled as a retrograde burn relative to Moon-relative velocity.

Phase 1: Launch and Ascent

Phase 1 focused on a simplified 1D vertical ascent model.

Model components
constant thrust during burn
variable mass due to propellant depletion
exponential atmosphere model
aerodynamic drag
gravity varying with altitude
Key findings
Burnout altitude was approximately 85 km
Burnout velocity was approximately 1.64 km/s
Maximum altitude was approximately 156 km
Maximum acceleration was approximately 25.5 m/s²
Maximum dynamic pressure occurred around 65.7 s at roughly 10.7 km altitude
Interpretation

The model showed physically sensible launch behaviour. Mass depletion caused acceleration to increase during the burn, and dynamic pressure peaked in the lower atmosphere as expected. This phase provided a useful first-order representation of early ascent.

Phase 2: Earth Orbit and Orbital Manoeuvres

Phase 2 extended the project into 2D orbital mechanics.

Model components
Earth-centred gravitational motion
circular orbit initialisation
RK4 orbital propagation
delta-v manoeuvres
orbit raising and two-burn circularisation
orbital energy analysis
Key findings
A stable 200 km circular orbit was reproduced successfully
Euler integration introduced visible orbital drift and energy oscillation
RK4 removed most numerical instability and preserved circular orbit behaviour
A prograde burn from circular orbit produced the expected elliptical transfer orbit
A second prograde burn at apoapsis circularised the raised orbit successfully
Interpretation

This phase demonstrated the importance of numerical method choice and provided a clean foundation for the translunar mission phase.

Phase 3: Translunar Transfer and Lunar Capture

Phase 3 developed the Earth–Moon mission model.

Model components
Earth departure from low Earth orbit
translunar injection burn
moving Moon model
Moon phase-angle sweeps
lunar gravity
lunar encounter corridor targeting
lunar impact detection
lunar orbit insertion burn
Moon-relative capture analysis
Key findings
Earth-only departure trajectories could easily reach lunar distance, but not necessarily the Moon itself
Moving-Moon targeting showed strong sensitivity to phase angle and burn timing
A refined phase and departure configuration produced near-perfect arrival into a chosen lunar encounter corridor
Including lunar gravity revealed the need for LOI to avoid impact or uncontrolled flyby
A successful non-impacting captured lunar trajectory was achieved using a tuned LOI burn
Best capture case

One successful capture configuration used:

burn time = 3000 s
translunar delta-v = 3370 m/s
Moon phase angle = 5.910 rad
target lunar altitude = 3000 km
LOI delta-v = 1700 m/s
LOI trigger distance ≈ 9475 km

This produced:

no lunar impact
negative Moon-relative specific energy
a bound lunar trajectory
encounter error of approximately 1 km relative to the target lunar orbit radius
Key Results
Built a complete multi-phase mission simulation from ascent to lunar capture
Demonstrated the difference between Earth-only, fixed-Moon, and moving-Moon targeting
Identified strong sensitivity of translunar trajectories to both phase angle and delta-v
Upgraded the project from Euler integration to RK4 for improved numerical stability
Achieved a successful simplified lunar capture with lunar gravity and LOI
Limitations
Two-dimensional model only
Impulsive burns rather than finite-duration thrust modelling
Simplified circular Moon orbit
No solar perturbations or non-spherical gravity effects
Captured lunar orbit remains very low and would need further refinement for operational realism
Future Improvements
Refine LOI strategy to produce a higher and safer lunar perilune
Add finite burn modelling
Extend the simulation into 3D
Include additional perturbations such as solar gravity
Add trans-Earth injection and return trajectory modelling
Introduce optimisation methods for automatic trajectory tuning
How to Run

Clone the repository and run the desired phase script with Python.

Example:

python phase3/phase3_loi.py

If a launcher script is added later, all phases can also be run through:

python main.py
Why this project matters

This project was built to go beyond standard classroom orbital mechanics problems and develop a practical understanding of mission design, numerical simulation, and iterative engineering refinement. It demonstrates not just theoretical knowledge, but the ability to build, test, debug, and improve a complex aerospace simulation.
