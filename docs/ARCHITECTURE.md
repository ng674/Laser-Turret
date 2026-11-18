# Architecture

## Functional pipeline

```text
frames -> detector -> association/filtering -> confirmed tracks -> selector
       -> logs/metrics                              |
                                                   v
                                  calibration -> desired bearing
                                                   |
                                      +------------+------------+
                                      |                         |
                                 fake/MuJoCo plant       disabled hardware adapter
                                      |                         |
                                      +---------- telemetry ----+
```

## Stable boundary between contributors

Track A owns frames through `TrackSnapshot` output. Track B owns desired-bearing
control through simulated telemetry. The calibration adapter between image-space
tracks and bearings is integrated only after camera calibration data exists.

Neither side imports the other's concrete implementation. Shared dataclasses and
protocols live directly under `src/laser_turret/`; changes to them are reviewed by
both contributors before either branch depends on the change.

## Coordinate rules

- Image pixels: origin top-left, +x right, +y down.
- Normalized image coordinates: both axes in `[0, 1]`.
- OpenCV camera frame: +x right, +y down, +z forward.
- Joint positions: radians, with measured zero and direction.
- Time: monotonic seconds inside sessions; wall-clock time only in metadata.

No implicit conversion between pixels, normalized coordinates, degrees, radians,
or servo units is permitted.

## Runtime modes

- `VISION_ONLY`: frames, detections, tracking, selection, logging; no actuation.
- `SIMULATION`: controller connected only to fake plant or MuJoCo.
- `HARDWARE_DISABLED`: protocol/telemetry tests with no physical output enabled.

Hardware motion is a later gated mode. Optical-source activation is outside the
autonomous perception/control path.

## Data and experiment reproducibility

Every run records configuration, source-session identity, code commit, random
seed, timings, and metrics. Raw recordings are immutable and excluded from Git;
manifests and small generated fixtures are versioned. Dataset splits are made by
recording session to prevent adjacent-frame leakage.
