# Work Track B - CAD and Simulation

## Mission

Build a reproducible two-axis digital twin of the current V8 turret geometry and
a deterministic controller baseline. Work must remain independent of the camera
implementation so both branches can merge through the shared interfaces.

This track does **not** connect to physical motors or activate an optical source.
Its outputs are simulation code, MJCF/assets, tests, configuration, and telemetry.

## What exists now

- The repository runs without third-party packages: `make test` and `make demo`.
- Shared observation contracts live in `src/laser_turret/models.py`.
- Coordinate and message semantics are in `docs/INTERFACES.md`.
- The current mechanical source is `cad/turret_v8_K1Max/cad/main.scad`.
- Existing STL and 3MF files are print artifacts, not an articulated simulator.
- `simulation/` contains reserved locations for MuJoCo models, simplified assets,
  and deterministic fixtures.
- No fake plant, controller, MJCF model, calibrated camera transform, measured
  joint dynamics, or hardware adapter has been implemented yet.

## Required reading before edits

Read these files in order and inspect the referenced source rather than relying
only on this summary:

1. `README.md`
2. `docs/PROJECT_CONTEXT.md`
3. `docs/ARCHITECTURE.md`
4. `docs/INTERFACES.md`
5. `cad/README.md`
6. `cad/turret_v8_K1Max/README.md`
7. `cad/turret_v8_K1Max/cad/main.scad`
8. `cad/turret_v8_K1Max/reference/servo_dimensions.jpg`
9. `hardware/PARTS.md`
10. `config/default.toml`
11. `pyproject.toml`

The older V5 audit under the CAD reference directory documents unresolved history;
`hardware/PARTS.md` and the current V8 CAD/handoff take precedence when they differ.

## Branch and ownership

Create `feature/simulation-model` from the latest `origin/nikil-dev`.

Owned paths:

```text
simulation/
src/laser_turret/simulation/
src/laser_turret/control/
tests/test_simulation*.py
tests/test_control*.py
```

`cad/` may be changed only for a documented CAD correction or a reproducible
simulation export. Preserve the original V8 package. Do not edit camera-owned
`detection/`, `tracking/`, `evaluation/`, or their tests.

Shared files requiring coordination with Nikil:

```text
src/laser_turret/models.py
config/default.toml
docs/INTERFACES.md
pyproject.toml
```

If one must change, isolate the contract change in a small commit before writing
code that depends on it.

## Machine prerequisites

Required:

- Git
- Python 3.11 or newer
- A shell capable of running `make` and Python virtual environments

Installed by the repository's simulation bootstrap:

- Project package in editable mode
- `mujoco>=3.2`
- `gymnasium>=1.0`
- `pytest>=8.0`, `ruff>=0.8`, and `mypy>=1.13`

Optional but needed when converting or visually checking CAD:

- OpenSCAD with command-line access
- A desktop/OpenGL environment for interactive MuJoCo viewing

Do not install OpenSCAD or other system packages automatically. If it is absent,
continue with the fake plant and MJCF primitives, then ask the user before a
system-level installation.

## Setup from a fresh clone

```bash
git clone https://github.com/ng674/Laser-Turret.git
cd Laser-Turret
git switch nikil-dev
git pull --ff-only

make test
make setup-sim
make check-sim
```

`make setup-sim` creates `.venv`, upgrades packaging tools, and installs the
`sim` and `dev` optional dependencies from `pyproject.toml`. `make check-sim`
verifies imports/versions and runs the shared test suite.

Manual equivalent:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e '.[sim,dev]'
python scripts/check_simulation_environment.py
make test
```

## Mechanical model context

- OpenSCAD units are millimeters; MuJoCo units are SI, so convert lengths to meters.
- The mechanism has two revolute degrees of freedom: pan and tilt.
- The camera is mounted away from the pan/tilt axes; pixels cannot be treated as
  joint angles. Keep camera extrinsics explicit and provisional until calibrated.
- The V8 OpenSCAD assembly contains print/manufacturing detail. The simulation
  should use primitives or simplified meshes for the foundation, pan carrier,
  tilt head, and camera body.
- Do not use grouped print-batch STLs as articulated bodies.
- Joint limits, inertial properties, center of mass, damping, friction, backlash,
  servo lag, and feedback noise are not physically measured yet. Put provisional
  values in a clearly labeled configuration/model section and make them easy to
  replace.

## Implementation sequence

### Phase B1 - dependency-free fake plant

Implement first:

```text
src/laser_turret/simulation/plant.py
src/laser_turret/control/pid.py
tests/test_simulation_plant.py
tests/test_control_pid.py
```

The fake plant models pan/tilt position and velocity, timestep, configurable
actuator lag, bounded velocity/acceleration, soft limits, and observation noise.
The controller must expose explicit `DISABLED`, `HOLD`, and active states.

Acceptance criteria:

- deterministic with a seed;
- never exceeds configured joint/rate limits;
- stale or invalid input enters `HOLD`;
- disabled output cannot move the plant;
- scripted bearings converge without unstable oscillation;
- standard-library tests pass without MuJoCo installed.

### Phase B2 - simplified CAD-to-MuJoCo model

Expected outputs:

```text
simulation/mujoco/turret.xml
simulation/mujoco/README.md
simulation/assets/                 optional simplified meshes only
simulation/fixtures/               scripted target motions
src/laser_turret/simulation/mujoco_plant.py
tests/test_simulation_mujoco.py
```

Build a fixed base, pan hinge, tilt hinge, head, and camera transform. Use MJCF
defaults for readable repeated properties. Record every source dimension,
millimeter-to-meter conversion, assumed mass/inertia, joint axis, zero pose, and
provisional value in `simulation/mujoco/README.md`.

Acceptance criteria:

- MJCF loads without warnings/errors;
- exactly two actuated revolute joints represent pan and tilt;
- joint axes and zero pose agree with the documented OpenSCAD interpretation;
- limits are enforced in the model and controller;
- camera body/site is attached to the correct simulated frame;
- head follows scripted commands without detached or duplicate bodies;
- headless test runs do not require an interactive viewer.

### Phase B3 - common adapter and telemetry

The fake plant and MuJoCo plant must implement the same local protocol. Log
monotonic timestamp, command, measured joint state, mode, limit state, and faults.
Use synthetic desired bearings until Track A supplies recorded tracks.

Do not implement the pixel-to-bearing calibration by guessing a field of view.
That adapter is an integration phase after camera calibration exists.

## Integration contract with Track A

Track A will eventually produce replayable timestamped `TrackSnapshot` records.
Integration adds a separate calibration adapter:

```text
TrackSnapshot -> calibrated desired bearing -> controller -> simulated plant
```

Simulation code must not import OpenCV or detector implementations. Camera code
must not import MuJoCo. Shared integration fixtures belong in `tests/fixtures/`.

## Required tests and commands

During development:

```bash
make test
make check-sim
git diff --check
```

Before a pull request:

```bash
make check
make check-sim
git status --short
```

The pull request must include exact commands run, observed results, assumptions,
and unresolved physical measurements. Do not claim real-world accuracy from the
unvalidated digital twin.

## First pull request boundary

The first pull request ends after Phase B1. It must contain the fake plant,
bounded controller, tests, and short usage documentation. Do not bundle the full
MuJoCo conversion into that same pull request. This gives the camera branch a
stable simulated consumer while the CAD model proceeds independently.

## Prompt to give Codex

From the repository root, the contributor can start a Codex session with:

> Read `AGENTS.md` and then read `TRACK_SIMULATION.md` completely. Perform a
> read-only preflight of every required source listed there. Report the current
> repository state, assumptions, exact Phase B1 files you propose changing, and
> the tests you will add. Do not edit files, install packages, create a branch,
> commit, or push until I approve that preflight.
