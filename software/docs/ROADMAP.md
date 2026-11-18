# Incremental project roadmap

The platform is a partially observable, dynamic, continuous environment. Camera
measurements are noisy and delayed, the target can be occluded, and the joints
have backlash and saturation. That framing determines which CS 530 methods are
useful and where.

## Phase 0 - freeze contracts and collect data (now)

Deliverables:

- repository structure, coordinate conventions, experiment log format;
- 10-20 short recordings of approved objects under different lighting, motion,
  distance, clutter, and partial occlusion;
- a calibration board recording and a stationary-camera noise recording;
- a labeled test subset held out by recording session.

Course connection: agents/environments; data, noise, and DNN evaluation. This is
where train/validation/test leakage and the limits of the sensor are established.

Exit gate: every recording has metadata; held-out sessions are never used for
tuning; target classes exclude people and faces.

## Phase 1 - detection and multi-object tracking (first build)

Pipeline:

```text
video -> detector -> association -> Kalman filter -> track lifecycle -> metrics
```

Start with a color/shape detector for plumbing and debugging. Replace it with a
transfer-learned detector only after the tracker and evaluation harness work.
Track in image space with a constant-velocity Kalman filter. Compare raw centroid
jitter with filtered jitter and measure identity switches through occlusion.

Course connection:

- lectures 2-5: supervised learning, DNNs, feature spaces, robustness;
- lectures 6-9: hidden/discrete state ideas, filtering, state-space models,
  Kalman filtering, noise, and sensor fusion.

Do not force every technique into production. An HMM is useful as a small track
state model (`tentative`, `confirmed`, `occluded`, `lost`), while the continuous
position/velocity estimate belongs in a Kalman filter.

Exit gate: on held-out recordings, report precision/recall, center error, track
fragmentation, ID switches, jitter, and end-to-end latency. Thresholds should be
set after the first baseline rather than invented now.

## Phase 2 - camera and kinematic calibration

Deliverables:

- camera intrinsics and distortion coefficients;
- measured camera-to-pan/tilt transform;
- pixel-to-bearing conversion with uncertainty;
- measured joint zero, direction, soft limits, speed, deadband, and backlash;
- replay test that converts known board points to expected bearings.

Use classical geometry here. ML does not replace calibration. Fuse analog servo
feedback with commanded state only after characterizing their noise.

Exit gate: bearing error is measured across the usable field of view; all guessed
CAD dimensions are either replaced by measurements or marked uncertain.

## Phase 3 - MuJoCo digital twin

Build a simplified collision/visual model from the V8 OpenSCAD assembly. Use
primitive bodies or decimated meshes, not print-layout meshes. Model two hinge
joints, camera offset, joint limits, actuator lag, backlash approximation, and a
moving target. Match the same observation and desired-bearing interfaces used by
the real system.

Course connection: utility/value iteration for small discretized sanity checks;
Monte Carlo evaluation for noisy trials; planning and learning; model-based
reasoning.

Exit gate: deterministic controller follows scripted targets in simulation;
simulation logs can be replayed through the same evaluator as recorded video.

## Phase 4 - deterministic controller before RL

Implement a rate-limited PID or image-based visual-servo controller. This is the
baseline that any learned policy must beat. Include joint/rate limits, anti-windup,
lost-track `HOLD`, watchdogs, and an explicit disabled output state.

Course connection: utility and decision-making. Define cost from pointing error,
motion/energy, limit proximity, jerk, and loss of target.

Exit gate: stable simulation tracking over the target-speed envelope with no
limit violations and acceptable overshoot/settling time.

## Phase 5 - learning experiments in simulation

Only after the deterministic baseline:

- Monte Carlo: evaluate expected return and uncertainty over randomized episodes.
- TD/Q-learning: use only for a deliberately discretized educational model.
- Dyna-Q/planning: compare real transitions with simulated replay.
- DNN approximation: continuous observations where a table is impossible.
- Policy gradients/actor-critic: optional continuous-rate policy experiment.
- MCTS: useful as a course comparison, usually excessive for fast visual servoing.
- robust feature/latent-space learning: experiment with occlusion or appearance
  variation only if the detector is the limiting subsystem.

Randomize lighting, texture, camera noise/delay, mass, friction, servo lag,
backlash, and target motion. Keep a separate nominal validation distribution.

Exit gate: a learned method beats the deterministic baseline on predefined held-
out scenarios and remains inside every safety constraint. Otherwise retain PID.

## Phase 6 - hardware-in-the-loop, laser-free

Bring up one subsystem at a time:

1. Pico connected, servos physically disconnected: verify protocol/watchdog.
2. One unloaded servo at low rate: verify direction, feedback, stop, and limits.
3. Two unloaded axes: verify power behavior and stop.
4. Assembled mechanism with LED dummy and clamped base.
5. Camera and motion together with conservative speed/angle limits.
6. Recorded target replay, then a slow approved physical object.

Exit gate: manual enable/stop works independently; disconnects and stale commands
go to a safe hold/disable state; thermal/current and mechanical behavior are
logged; no optical source is installed.

## Phase 7 - final integration boundary

Keep object tracking, motion control, and optical-source permission as separate
subsystems. This software project does not autonomously activate an optical
source. Any future source must be independently qualified, normally off, and
subject to physical access control and hardware permission circuitry.

## What to do while parts print

- Record and label the initial object videos.
- Establish the Phase 1 metrics and tracker baseline.
- Print a paper calibration board and capture calibration footage.
- Convert only the V8 pan/tilt/camera geometry into a first MuJoCo XML model.
- Define the Pico message schema and write a fake serial device.
- Build dashboards from saved logs; avoid live hardware dependencies.
- Measure delivered components and update a dimension ledger.
- Run fit coupons before committing to full assembly.

