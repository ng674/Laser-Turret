# Project context

## Mission

Build a two-axis camera-based object-tracking research platform in small,
testable increments. Begin with offline perception and state estimation, then add
a CAD-derived MuJoCo digital twin, then hardware-in-the-loop motion. Treat any
optical source as a separate, normally-off subsystem. Use an LED or screen
reticle for all development and calibration.

## Current state

- Mechanical source of truth: `../turret_v8_K1Max/cad/main.scad`.
- Nominal printed assembly: 14 pieces in two K1 Max print batches.
- Camera location in the OpenSCAD model is offset from the pan/tilt axes; do not
  assume camera pixels map directly to joint angles.
- The CAD and servo/horn interfaces are provisional pending physical measurement.
- Procurement planning recommends a laser-free motion/vision milestone first.
- No motor firmware, webcam calibration, automatic timeout, or real-world target
  tracking has yet been demonstrated.
- Software increment 0 is present: a dependency-free constant-velocity Kalman
  tracker and nearest-neighbor multi-object association.

## Architecture rule

Keep these layers independent and testable:

```text
recorded/live frames -> detector -> tracker -> target selector -> desired bearing
                                            -> logger/evaluator

desired bearing -> simulated plant OR disabled hardware adapter -> telemetry
```

The perception layer must never write servo PWM/serial commands. A controller may
only consume a typed desired-bearing message after the simulator and hardware
safety gates pass.

## Safety constraints

- Default operating mode is `SIMULATION` or `VISION_ONLY`.
- No face/person class is eligible for target selection.
- Do not implement autonomous optical-source activation.
- Use a visible on-screen reticle or low-power LED dummy for alignment work.
- Hardware motion requires joint limits, rate limits, loss-of-track timeout,
  manual enable, independent stop, and a stable clamped base.
- A lost, stale, low-confidence, or out-of-bounds target means `HOLD`, never
  continued prediction-driven motion.
- Keep power actuation and perception in separate processes/interfaces.

## Engineering conventions

- Python 3.11+; type annotations on public functions.
- Keep the core tracking math independent of OpenCV, PyTorch, and MuJoCo.
- Every experiment records configuration, input identity, metrics, and seed.
- Train/validation/test data must be split by recording session, not random frame,
  to prevent near-duplicate leakage.
- Prefer recorded data and replayable tests before live camera work.
- New features need a unit test or a recorded replay acceptance test.
- Do not silently replace the mechanical source of truth or guessed dimensions.

## Current two-person milestone

- Person A owns recorded-video perception and tracking evaluation.
- Person B owns the MuJoCo-independent simulation plant and controller baseline,
  followed by the CAD-derived MuJoCo model.
- Both implement against `docs/INTERFACES.md` and avoid editing shared contracts
  without coordinating the change first.

