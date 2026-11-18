# Software and hardware interfaces

All layers communicate through timestamped messages. Adapters may change, but
these meanings should not.

## Coordinate frames

- `image_px`: origin top-left, +x right, +y down.
- `image_norm`: x and y in `[0, 1]` using actual frame width/height.
- `camera`: +z forward, +x right, +y down (OpenCV convention).
- `base`: define during MuJoCo conversion and document against the CAD axes.
- `joint`: pan and tilt radians with measured zero/direction and hard/soft limits.

Never mix pixels, normalized image coordinates, degrees, radians, or servo units
without an explicit conversion function.

## Detection

Required fields: monotonic timestamp, frame ID, label, confidence, bounding box in
pixels. A detector has no knowledge of motors or target selection.

## Track

Required fields: stable track ID, label, filtered center, velocity, covariance,
age, hits, misses, and confirmed flag. Predictions may bridge short detection
gaps for display and association, but stale predictions are not permission for
continued physical motion.

## Selected target

Target selection is an explicit policy over confirmed tracks and a whitelist of
non-person labels. Output is either one track reference or `None`. Selection does
not imply actuation.

## Desired bearing

Calibration converts a selected image observation to pan/tilt bearing plus an
uncertainty estimate. If calibration is absent, stale, or out of range, output is
invalid. The controller must reject invalid bearings.

## Controller command

Simulation and hardware adapters consume the same rate/position command shape,
but the hardware adapter defaults disabled. Every command includes a sequence,
timestamp, expiry, mode, and bounded pan/tilt values. Missing or expired commands
produce `HOLD` or hardware disable.

## Telemetry

Log measured joint positions, requested commands, limit/stop state, voltage/current
when available, mode, fault flags, and timing. Logs use monotonic time internally
and include wall-clock session metadata.

## MuJoCo asset path

Use `../../turret_v8_K1Max/cad/main.scad` as the geometric reference. Export or
create simplified bodies for the foundation, pan carrier, tilt head, and camera.
Exclude print batches, support geometry, electronics clutter, fastener detail,
and duplicate historical revisions. Record every simplification and measured
joint transform in the model README.

