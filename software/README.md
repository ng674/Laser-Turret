# Laser Turret software workspace

This folder is the software source of truth for the project. Work on it directly
from the Laser Turret folder in VS Code/Codex, not from a historical CAD revision.

The first increment is deliberately hardware-free: detections enter the tracker,
and stable tracks come out with an ID, position, velocity, and uncertainty. No
motor or optical-source command is produced.

## Start here

1. Read `PROJECT_CONTEXT.md`, `docs/COLLABORATION.md`, and `docs/ROADMAP.md`.
2. Run the dependency-free tests:

   ```bash
   PYTHONPATH=src python3 -m unittest discover -s tests -v
   ```

3. Run the synthetic tracking demo:

   ```bash
   PYTHONPATH=src python3 -m laser_turret.demo
   ```

4. Choose Person A or Person B in `docs/COLLABORATION.md`. Do not begin live motor
   control until the acceptance gates in `docs/ROADMAP.md` pass.

## Layout

```text
software/
  PROJECT_CONTEXT.md         Shared context and non-negotiable constraints
  pyproject.toml             Python package and future optional dependencies
  config/default.toml        Coordinate, tracker, and safety defaults
  data/README.md             Dataset layout and leakage rules
  docs/ROADMAP.md            Incremental build and CS 530 technique mapping
  docs/COURSE_MAP.md         Every Fall 2026 lecture mapped to an experiment
  docs/COLLABORATION.md      Two-person ownership and merge workflow
  docs/INTERFACES.md         Contracts between perception, sim, and hardware
  src/laser_turret/
    models.py                Detection and track data contracts
    tracking/kalman.py       Constant-velocity Kalman filter
    tracking/manager.py      Multi-object association and track lifecycle
    demo.py                  Hardware-free synthetic demo
  tests/                     Dependency-free unit tests
```

`firmware/` should be added only when its corresponding roadmap increment begins;
this keeps the initial work focused on independently testable software.

## Mechanical source of truth

The current mechanical handoff is `../turret_v8_K1Max/`. Its OpenSCAD assembly is
the starting point for later MuJoCo geometry conversion. Dimensions remain
provisional until the printed fit coupons and delivered components are measured.


