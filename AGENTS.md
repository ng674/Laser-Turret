# Repository instructions for Codex

## Required orientation

Before changing this repository, read:

1. `README.md`
2. `docs/PROJECT_CONTEXT.md`
3. `docs/ARCHITECTURE.md`
4. `docs/INTERFACES.md`
5. The work-track file matching the requested task

For CAD, simulation, MuJoCo, plant, controller, or 3D-model work, you MUST read
`TRACK_SIMULATION.md` completely before planning or editing. Also inspect the live
files it lists as required sources. For camera, detection, tracking, or evaluation
work, read `TRACK_CAMERA.md` instead.

## Shared engineering rules

- Work from the live repository; do not assume instructions from another clone.
- Preserve the two-track ownership boundary. Do not edit the other contributor's
  paths unless the user explicitly requests integration work.
- Treat `src/laser_turret/models.py`, `config/default.toml`, and
  `docs/INTERFACES.md` as shared contracts. Propose contract changes separately.
- Add or update tests for behavioral changes.
- Run `make check` before reporting completion.
- Do not commit, push, change branches, install system packages, or modify remote
  state without the user's explicit approval.
- Record provisional physical values as provisional. Never invent missing mass,
  inertia, joint-limit, camera-transform, servo, horn, or fastener measurements.

## Safety and scope

- Default modes are `VISION_ONLY`, `SIMULATION`, or `HARDWARE_DISABLED`.
- People and faces are never selectable target classes.
- Perception modules do not issue motor commands.
- Simulation/controller work must implement limits, stale-input handling, and a
  disabled/hold state before any hardware adapter is considered.
- Do not implement autonomous optical-source activation. Initial physical work
  uses a screen reticle or LED dummy and is outside the current simulation phase.
