# Work Track A - Camera Detection and Tracking

This track owns the complete path from recorded camera frames to replayable,
timestamped object tracks. It does not own motor control or MuJoCo.

## Branch and owned paths

Create `feature/camera-tracking` from the latest `nikil-dev`.

```text
src/laser_turret/detection/
src/laser_turret/tracking/
src/laser_turret/evaluation/
data/
tests/test_detection*.py
tests/test_tracker*.py
tests/test_evaluation*.py
```

Do not edit simulation/control modules. Changes to `models.py`, configuration
schemas, or `docs/INTERFACES.md` must be isolated in a small contract commit and
agreed with the simulation owner before dependent work continues.

## Run the shared baseline

```bash
make test
make demo
```

For OpenCV work:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[vision,dev]'
```

## Deliverables

- [ ] Add a `Detector` protocol that outputs the existing `Detection` type.
- [ ] Add a recorded-video source with monotonic timestamps and frame IDs.
- [ ] Add a simple color/shape detector as the observable baseline.
- [ ] Log detections and `TrackSnapshot` records to a documented JSONL format.
- [ ] Add session-level dataset manifests; never split adjacent video frames
      across train, validation, and test sets.
- [ ] Report precision, recall, center error, jitter, ID switches,
      fragmentation, loss/reacquisition behavior, and end-to-end latency.
- [ ] Add a transfer-learned detector behind the same protocol only after the
      simple baseline and evaluator work.

## Output contract for integration

The simulation contributor receives a replayable sequence containing timestamp,
frame ID, track ID, label, filtered position, velocity, covariance, age, hits,
misses, and confirmation state. Camera code never imports MuJoCo, serial, or
hardware-control modules.

## Definition of done for the first pull request

One checked-in synthetic or tiny generated fixture runs through frame source,
detector, tracker, logger, and evaluator without a webcam. Tests pass with
`make test`, and the pull request includes the exact replay command and metrics.
