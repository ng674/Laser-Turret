# Laser Turret Research Platform

Two-axis camera-tracking research platform with a shared perception API, a
CAD-derived MuJoCo model, and a staged path to laser-free hardware-in-the-loop
testing. The repository is organized so camera tracking and simulation can be
developed independently and joined through stable, timestamped interfaces.

## Start here

```bash
git clone https://github.com/ng674/Laser-Turret.git
cd Laser-Turret
git switch nikil-dev
make test
make demo
```

The current tests and synthetic tracker demo use only Python's standard library.
Optional vision and simulation dependencies are installed only when their work
track needs them:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[vision,sim,dev]'
```

## Choose one work track

- Camera and tracking owner: read [`TRACK_CAMERA.md`](TRACK_CAMERA.md).
- CAD and simulation owner: read [`TRACK_SIMULATION.md`](TRACK_SIMULATION.md).

Both contributors must also read [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
and [`docs/INTERFACES.md`](docs/INTERFACES.md). Those files define the boundary
that lets both branches merge cleanly.

Codex automatically receives the durable repository instructions in
[`AGENTS.md`](AGENTS.md). For simulation work, those instructions require Codex
to read `TRACK_SIMULATION.md` and its source list before proposing changes.

Simulation contributor setup:

```bash
make setup-sim
make check-sim
```

## Repository layout

```text
Laser-Turret/
  src/laser_turret/       Python package: detection, tracking, control, simulation
  tests/                  Unit and later cross-track integration tests
  scripts/                Contributor setup and environment verification
  config/                 Versioned runtime and safety defaults
  data/                   Dataset manifests; recordings remain untracked
  simulation/             MuJoCo XML, simplified assets, and scenarios
  cad/turret_v8_K1Max/    Current OpenSCAD source, STLs, 3MFs, and validation
  hardware/               Parts source, procurement notes, and hardware context
  docs/                   Architecture, interfaces, course map, and roadmap
  models/                 Local trained weights; ignored except placeholders
  runs/                   Local experiment output; ignored except placeholders
```

## Current baseline

- Typed `Detection` and `TrackSnapshot` contracts.
- Dependency-free constant-velocity Kalman filter.
- Multi-object nearest-neighbor tracker with track confirmation and expiry.
- Synthetic tracking demo and five passing unit tests.
- V8 K1 Max mechanical source and print handoff.
- Parts/procurement context stored under `hardware/`.

The next camera milestone is recorded-video detection and evaluation. The next
simulation milestone is a dependency-free two-axis fake plant before MuJoCo.

## Safety boundary

Development defaults to `VISION_ONLY` or `SIMULATION`. People and faces are not
eligible target classes. Perception code cannot command motors, and this project
does not autonomously activate an optical source. Initial physical integration
uses an on-screen reticle or LED dummy, bounded motion, independent stop controls,
and a clamped base.
