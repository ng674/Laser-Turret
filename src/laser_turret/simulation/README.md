# Person B workspace

Begin with the dependency-free fake two-axis plant in `plant.py`. Add MuJoCo
assets only after this plant, the controller, and their tests stay stable.

`TwoAxisPlant.step` advances pan and tilt. An `ACTIVE` command is lagged, then
tracked subject to provisional rate, acceleration, and soft-limit caps. `HOLD`
and an expired command brake to a stop. `DISABLED` freezes the joints and
zeroes the rate. `measure` adds seeded observation noise; `pan_rad` and
`tilt_rad` stay the true state.

These constants are provisional and unmeasured:

- pan soft limits, ±90 degrees
- tilt soft limits, ±45 degrees
- max rate, 180 degrees/second
- max acceleration, 720 degrees/second²
- actuator lag, 40 ms

They are not a claim about the Waveshare drawing or the DFRobot servo in the
parts ledger. Replace them when the mechanism is measured.

```python
from laser_turret.control import ControlMode, JointCommand
from laser_turret.simulation import TwoAxisPlant

plant = TwoAxisPlant(seed=530, observation_stddev_rad=0.0)
command = JointCommand(
    sequence=1,
    timestamp_s=0.0,
    expiry_s=1.0,
    mode=ControlMode.ACTIVE,
    pan_rad=0.35,
    tilt_rad=0.07,
)
state = plant.step(command, 0.01)
```

Run `make test`. The tests do not need MuJoCo.
