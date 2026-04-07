Graph Interpretation



**Altitude vs time**

This graph shows how the rocket climbs during powered ascent and then continues to gain altitude after burnout due to inertia.



**What it means**

* During the burn, altitude rises faster and faster because the rocket is accelerating upward.
* At burnout, the engine stops producing thrust.
* Even after burnout, the rocket still rises because it has significant upward velocity.
* Eventually gravity reduces the velocity to zero, and the rocket reaches maximum altitude.



**Significance of result**

(Outputs found in 1D\_Output.txt)



The burnout altitude of 85.3 km means the vehicle has climbed through most of the atmosphere before propulsion ends.

The maximum altitude of 154.6 km shows that the coasting phase contributes a lot to the total altitude reached.



**-------------------------------------------------------------------------------------------------------------------------------------**



**Velocity vs time**

This graph shows how quickly the rocket is moving upward.



**What it means**

* Velocity increases during powered ascent because thrust is greater than the combined effects of gravity and drag.
* As the rocket gets lighter, the same thrust produces more acceleration, so velocity rises more rapidly later in the burn.
* Around burnout, velocity reaches its highest value.
* After burnout, velocity begins to fall because there is no more thrust, only gravity and drag acting against the motion.



**Significance of result**

A burnout velocity of 1629.3 m/s and maximum velocity of 1631.8 m/s being very similar suggests:

* peak speed occurs near burnout
* after that, the rocket is mostly coasting, not accelerating



**-------------------------------------------------------------------------------------------------------------------------------------**



**Acceleration vs time**

this graph is pretty cool



**What it means**

Acceleration is determined by:

**(T - D - mg) / m**



**Why it changes**

* Early in flight, the rocket is heavy, so acceleration is lower.
* As fuel burns off, mass decreases.
* If thrust stays constant, then acceleration increases because the denominator gets smaller.
* Drag can temporarily reduce acceleration, especially in denser atmosphere.
* After burnout, acceleration becomes negative because thrust drops to zero and gravity dominates.



**Significance of result**

The maximum acceleration is 25.19 m/s², or roughly 2.57 g.



**-------------------------------------------------------------------------------------------------------------------------------------**



**Mass vs time**

This graph should show a straight-line decrease during the burn, then flatten after burnout.



**What it means**

* Propellant is being consumed at a constant mass flow rate.
* Once the burn ends, the mass stops changing because the fuel is gone.



**Why it matters**

This graph is important because it explains why acceleration rises during the burn. It links the propulsion model directly to the motion.



**-------------------------------------------------------------------------------------------------------------------------------------**



**Drag vs time**

this is the graph that links closely to my course and im excited to see it physically 



**What it shows**

* drag starts near zero because velocity is near zero
* drag rises as velocity increases
* drag peaks at about 65.7 s
* drag then falls as atmospheric density drops away



**Engineering significance**

This shows that peak aerodynamic loading occurs before burnout and much lower in the atmosphere.



**Dynamic pressure vs time**



This is the Max Q plot.



**What it shows**

* dynamic pressure rises during early ascent
* reaches a peak at 65.7 s
* then falls off as the atmosphere thins



**Engineering significance**

Max Q is a key launch event because it represents maximum aerodynamic stress on the vehicle. In real missions, engines may throttle around Max Q to reduce loads. This model does not include throttling yet, but the fact that it identifies a sensible Max Q point is great.







