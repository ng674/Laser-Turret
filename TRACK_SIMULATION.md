# Work Track B - CAD and Simulation

This track owns the two-axis plant model, deterministic controller baseline, and
CAD-to-MuJoCo conversion. It consumes synthetic or replayed perception outputs and
does not edit the detector or tracker.

## Branch and owned paths

Create `feature/simulation-model` from the latest `nikil-dev`.

```text
simulation/
src/laser_turret/simulation/
src/laser_turret/control/
tests/test_simulation*.py
tests/test_control*.py
cad/                       only for documented simulation exports or fixes
```

Treat `cad/turret_v8_K1Max/cad/main.scad` as the current geometric source of
truth. Dimensions and servo/horn fits remain provisional until measured. Changes
to shared message/configuration contracts require a small coordinated commit.

## Run the shared baseline

```bash
make test
make demo
```

For MuJoCo work:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[sim,dev]'
```

## Deliverables

- [ ] Implement a dependency-free two-axis fake plant first: position, velocity,
      acceleration/rate limits, actuator lag, soft limits, and observation noise.
- [ ] Implement a bounded PID or image-servo controller against synthetic desired
      bearings.
- [ ] Enforce stale-command expiry, lost-target `HOLD`, joint/rate limits, and an
      explicit disabled output state.
- [ ] Log commands and telemetry in a replayable format.
- [ ] Extract only the pan, tilt, camera, and base geometry needed for MuJoCo;
      use primitives or decimated meshes rather than print-layout meshes.
- [ ] Model two hinge joints, camera offset, measured/provisional limits, actuator
      lag, and target motion.
- [ ] Run the same controller API against the fake plant and MuJoCo adapter.

## Input contract for integration

Until camera output is available, generate synthetic timestamped targets matching
`docs/INTERFACES.md`. When Track A merges, replay its saved tracks through a
separate pixel-to-bearing/calibration adapter. Simulation and control code never
imports OpenCV or detector implementations.

## Definition of done for the first pull request

A deterministic test drives the fake plant toward scripted bearings, respects all
limits, and enters `HOLD` for stale input. Tests pass with `make test`; MuJoCo is
not required for this first pull request.
