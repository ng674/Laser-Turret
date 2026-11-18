# Simulation workspace

This directory is owned by the CAD/simulation work track.

Planned structure:

```text
simulation/
  mujoco/       MJCF models and scenarios
  assets/       simplified/decimated simulation-only meshes
  fixtures/     scripted targets and deterministic replay inputs
```

The first deliverable is a dependency-free fake two-axis plant under
`src/laser_turret/simulation/`, not a MuJoCo model. Once its controller contract
and tests are stable, reproduce the same interface with MuJoCo. See
`../TRACK_SIMULATION.md`.
