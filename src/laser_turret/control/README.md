# Person B workspace

Bounded simulation controllers live here. Outputs stay in simulation until the
roadmap's hardware gates are explicitly complete. This package does not read
camera pixels, command a servo driver, or enable an optical source.

`BoundedPID` starts in `DISABLED`. A fresh, valid bearing can be followed only
after `set_mode(ACTIVE)`. An invalid, non-finite, or stale bearing (older than
150 ms) produces `HOLD` and clears the integrators. Angles are radians.
Positive pan is to the right and positive tilt is up.

Degree aims convert at this boundary and nowhere else:

```python
from laser_turret.control import BoundedPID, ControlMode, bearing_from_degrees
from laser_turret.simulation import TwoAxisPlant

plant = TwoAxisPlant(seed=530)
controller = BoundedPID()
controller.set_mode(ControlMode.ACTIVE)
dt = 0.01
for step in range(300):
    now = step * dt
    bearing = bearing_from_degrees(timestamp_s=now, pan_deg=20.0, tilt_deg=4.0)
    command = controller.update(bearing, plant.pan_rad, plant.tilt_rad, now)
    plant.step(command, dt)
```

The default joint bounds match the provisional constants on `TwoAxisPlant`.
They are unmeasured stand-ins, not limits of a delivered servo. Run the
controller tests with `make test`.
