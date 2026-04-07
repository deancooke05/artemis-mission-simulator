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

## Project Structure

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
