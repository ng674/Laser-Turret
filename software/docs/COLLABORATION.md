# Two-person collaboration plan

The split follows the stable boundary between perception and a simulated plant.
Both people can work and test without waiting for the printed parts or editing the
same implementation files.

## Person A - perception and tracking

Own these paths:

```text
src/laser_turret/detection/
src/laser_turret/tracking/
src/laser_turret/evaluation/
data/
tests/test_detection*.py
tests/test_tracker*.py
tests/test_evaluation*.py
```

First deliverable:

1. Define a `Detector` protocol returning the existing `Detection` type.
2. Add a recorded-video adapter and simple color/shape detector.
3. Add JSONL/CSV track logging.
4. Measure detection precision/recall, center error, jitter, ID switches,
   fragmentation, and latency on session-held-out recordings.
5. Add a transfer-learned detector behind the same protocol only after the simple
   baseline works.

Person A's output to Person B is a replayable stream of timestamped
`TrackSnapshot` records. Person A does not import MuJoCo or issue motor commands.

## Person B - simulation and controller

Own these paths:

```text
src/laser_turret/simulation/
src/laser_turret/control/
sim/
tests/test_simulation*.py
tests/test_control*.py
```

First deliverable:

1. Implement a dependency-free two-axis fake plant with joint position, velocity,
   limits, lag, and configurable observation noise.
2. Implement a rate-limited PID/image-servo baseline against synthetic desired
   bearings.
3. Log controller command and plant telemetry using the shared coordinate rules.
4. Add lost/stale-target `HOLD`, command expiry, rate limits, and joint limits.
5. Convert only the V8 pan/tilt/camera geometry to MuJoCo after the fake-plant
   tests pass.

Person B consumes synthetic or recorded desired-bearing inputs. Person B does not
modify the detector or tracker and does not connect to physical motors yet.

## Shared files - coordinate before editing

These are the integration contract:

```text
src/laser_turret/models.py
docs/INTERFACES.md
config/default.toml
pyproject.toml
```

Nominate one integration owner, initially Nikil, for these files. If either
person needs a contract change, make it a small standalone commit and merge that
commit before continuing dependent work. Do not mix a contract change with a
large feature commit.

## Branches

Use `nikil-dev` as the integration branch. After it contains the agreed baseline,
create two feature branches from the same commit:

```bash
git switch nikil-dev
git pull --ff-only

# Person A
git switch -c feature/perception-tracking

# Person B, in a separate clone or worktree
git switch nikil-dev
git switch -c feature/simulation-control
```

Each person pushes only their feature branch. Merge small pull requests back into
`nikil-dev`; do not exchange ZIPs or copy entire folders over one another.

## Daily sync

At the start of a session:

```bash
git fetch
git rebase origin/nikil-dev
```

Before requesting a merge:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  python3 -m unittest discover -s tests -v
git diff --check
git status --short
```

Rebase only personal, unmerged feature commits. Never rewrite the shared
`nikil-dev` branch.

## Merge order for the first increment

1. Freeze the current `Detection` and `TrackSnapshot` contracts on `nikil-dev`.
2. Merge Person B's fake plant/controller baseline; it has no vision dependency.
3. Merge Person A's detector/replay/evaluation pipeline.
4. Add one small integration test that replays Person A's saved track data into
   Person B's simulated desired-bearing/controller path.
5. Tag the result `software-v0.1-vision-sim`.

## Definition of done

A branch is ready to combine when its tests pass independently, it does not edit
the other person's owned paths, it documents any new configuration, and it
includes a short sample command demonstrating the feature.

