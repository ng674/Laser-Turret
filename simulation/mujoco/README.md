# Simplified V8 turret in MuJoCo

`turret.xml` is a kinematic two-axis twin of `cad/turret_v8_K1Max/cad/main.scad`
built from box and cylinder primitives. It is for checking geometry, pointing,
and controller behaviour. It is not a validated dynamic model.

## Run

```bash
make setup-sim                                      # once: creates .venv with MuJoCo
.venv/bin/python -m mujoco.viewer --mjcf simulation/mujoco/turret.xml
.venv/bin/python simulation/mujoco/render_turret.py # headless PNGs in runs/mujoco/
.venv/bin/python simulation/mujoco/render_turret.py --pan-deg 30 --tilt-deg -15
```

In the viewer, open the Control panel and drag the `pan` and `tilt` sliders.

## Frames

- World frame = OpenSCAD assembly frame, mm converted to m. +Z up. At zero pose
  the emitter barrel and the camera both face world -Y.
- `pan` hinge: axis +Z, origin (0, 0, 68 mm) = foundation 8 + legs 50 + horn
  gap 10 (`main.scad` line 137). Positive pan turns the -Y aim toward +X.
- `tilt` hinge: axis +X of the pan frame, origin (-21, 0, 39) mm in the pan
  frame = carrier wall -31 + horn gap 10, height 39 (`main.scad` line 141).
  Positive tilt turns the aim downward. The OpenSCAD head geometry is mapped
  into the pan-aligned tilt body by (x, y, z) -> (z, y, -x), which is the
  `rotate([0,90,0])` on line 141.
- `base_camera`: fixed to the base at (125, -39, 153) mm, looking along -Y with
  image-up = +Z. It does not move with the turret.

## Source dimensions

| Body | Source in `main.scad` | Simplification |
|---|---|---|
| Foundation 230 x 100 x 8 mm, centre x = 60 | `shared_base()`, l. 68-80 | box; holes, slots, riser omitted |
| Legs at x = +/-46, 50 mm tall | `leg()`, l. 43-46 | two flanges + web |
| Servo deck 110 x 86 x 5 mm at z 58 | `base()`, l. 40-42 | box |
| Servo body 45.22 x 24.72 x 32 mm, axis offset 10.11 | l. 7-8, `servo_proxy()` | box (ST3215-HS drawing) |
| Horn d 19.2 x 3.2 mm, spacer d 19 x 6.8 mm | l. 12-14, 34 | cylinders |
| Carrier plate 66 x 76 x 5, wall 5 x 76 x 64 | `carrier()`, l. 48-52 | two boxes; gussets omitted |
| Head plates and saddle | `head()`, l. 55-63 | three boxes |
| Emitter barrel d 10.5 x 19 mm | l. 18, 141 | cylinder; nothing is emitted |
| Camera post, pad, 94 x 71 x 43.3 envelope | l. 89-107, 143-146 | boxes; envelope, not real shape |

Excluded: electronics tray, tray feet, switch cradle, breadboard, fasteners,
fit coupons, and print batches.

## Provisional values (none are measured)

- Mass: uniform density 1240 kg/m^3 (nominal PLA) for printed parts and
  1500 kg/m^3 for servo boxes. Infill, fasteners, and the real servo, camera and
  emitter masses are not modelled.
- Joint armature 0.001 kg m^2 and damping 0.002 N m s/rad stand in for gearbox
  inertia and friction.
- Position actuators: kp = 1.0 N m/rad, critically damped, no torque limit.
  Gravity leaves a small tilt offset (about 0.15 degrees at zero pose).
- Joint ranges copy the fake plant's provisional soft limits: pan +/-90,
  tilt +/-45 degrees.
- `base_camera` fovy = 45 degrees is a placeholder. Do not use it for
  pixel-to-bearing calibration.
- Collisions between turret parts are disabled; the model cannot detect
  self-interference at extreme poses.
- `hardware/PARTS.md` lists the DFRobot SER0044 servo, while the CAD uses the
  ST3215-HS outline. This model follows the CAD.

## Not yet done

`src/laser_turret/simulation/mujoco_plant.py`, the adapter that gives this model
the same `step(command, dt)` interface as `TwoAxisPlant`, and scripted target
fixtures.
