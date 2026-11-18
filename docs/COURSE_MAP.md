# CS 530 Fall 2026 technique map

Source course index: <https://firner.com/presentations/cs530/2026-Fall/>

The goal is to demonstrate the course's ideas with meaningful experiments, not
to place every algorithm in the final real-time path. Safety interlocks,
calibration, and basic control remain deterministic.

| Lecture | Course topic | Project use and evidence |
|---:|---|---|
| 1 | Principles of AI | Define the agent, observations, actions, environment properties, and success/failure metrics. |
| 2 | ML Review | Establish non-ML and simple-ML baselines; keep train/validation/test sessions separate. |
| 3 | Data, Noise, and DNNs | Measure camera/detector noise; write a dataset card; train a detector only after a data audit. |
| 4 | DNNs and Feature Spaces | Inspect detector embeddings/features and failure cases; compare frozen-backbone transfer learning with a simple detector. |
| 5 | Robust Feature Spaces | Test lighting, background, scale, motion blur, and occlusion shifts; use augmentation and later simulation randomization. |
| 6 | Discrete Space Filtering | Model track lifecycle as tentative/confirmed/occluded/lost; compare a rule-based lifecycle with an HMM experiment. |
| 7 | More Discrete Space Predictions | Use Viterbi or posterior smoothing offline to analyze recorded lifecycle sequences; do not use future observations in live control. |
| 8 | Noise and Fusion in State Space Models | Use the constant-velocity Kalman filter for image position and velocity; report covariance and jitter reduction. |
| 9 | Noise and Fusion | Characterize camera, timestamp, and servo-feedback noise; compare camera-only and fused state estimates. |
| 10 | Utility and Value Iteration | Define utility/cost and solve a small discretized pan/tilt benchmark; compare it with the deterministic controller. |
| 11 | Monte Carlo Control | Estimate policy return over many randomized simulation episodes; quantify confidence intervals and rare failures. |
| 12 | Monte Carlo | Demonstrate exploring starts and on/off-policy evaluation in the small simulated benchmark. |
| 13 | Temporal Difference Learning | Implement SARSA/Q-learning only in the discretized simulator and compare sample efficiency and conservatism. |
| 14 | Planning and Learning | Add a learned transition model or Dyna-Q experiment; compare real simulated steps with replayed/planned steps. |
| 15 | Mid-semester Review | Produce a milestone report that connects perception, filtering, utility, and evaluation results. |
| 16 | Decision-Time Planning | Test short-horizon rollout for target reacquisition or limit avoidance in MuJoCo. |
| 17 | Monte Carlo Tree Search | Optional benchmark for discrete decision-time planning; not the default 30 FPS controller. |
| 18 | RL with Approximation | Replace tables with a DNN value/Q approximator for continuous simulated observations; compare against PID. |
| 19 | Policy Learning with DNNs | Optional continuous-rate policy-gradient/actor-critic experiment in simulation only. |
| 20 | The Exploration Problem | Study epsilon schedules, curriculum, domain randomization, and coverage; exploration never runs on unrestricted hardware. |
| 21 | Learning and Reasoning | Treat the MuJoCo twin and learned dynamics as world models; test whether planning transfers across randomized dynamics. |

## Recommended final-project comparisons

Keep the experimental matrix small enough to finish:

1. Raw detector centroid vs Kalman-filtered track.
2. Simple detector vs transfer-learned detector under distribution shifts.
3. Deterministic PID/visual servo vs one learned policy in MuJoCo.
4. Nominal simulation vs domain-randomized simulation.
5. Simulation-only performance vs laser-free hardware replay.

This covers the course arc while preserving a credible engineering baseline.
