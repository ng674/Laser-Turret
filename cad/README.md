# CAD

`turret_v8_K1Max/` is the current mechanical source of truth. It contains the
editable OpenSCAD assembly, individual STL backups, two print batches, reference
dimensions, and validation reports.

For simulation, begin from `turret_v8_K1Max/cad/main.scad`. Build a simplified
kinematic model containing the base, pan hinge, tilt hinge, camera transform, and
moving head. Do not import grouped print-layout meshes as articulated bodies.

All servo, horn, shaft, bearing, and camera interfaces remain provisional until
delivered parts are measured. Preserve the original V8 package when exporting
simulation assets; place those exports under `simulation/assets/`.
