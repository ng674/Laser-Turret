# Parts and integration ledger

This ledger consolidates the supplied parts sheet with the repository's dated
procurement review. It records project context; it is not a checkout-ready bill
of materials.

## Core motion/vision milestone

| Subsystem | Current item or requirement | Planned quantity | Status |
|---|---|---:|---|
| Pan/tilt actuation | DFRobot SER0044 analog-feedback servo | 2 | Current cost-driven selection; mechanical equivalence and limits require verification |
| Controller | Raspberry Pi Pico H | 1 initially | USB motion controller; second board deferred with optical receiver work |
| Servo supply | Regulated 5 V, 4 A supply | 1 | Validate transient voltage/current with the actual servos; never parallel positive rails |
| Bearings | 608ZZ, 8 x 22 x 7 mm | 4 planned | Verify delivered dimensions and fits |
| Shafts | Ground 8 mm round steel stock | 1 pan plus 2 tilt stubs | Final lengths follow measured assembly stack |
| Retention | 8 mm collars, spacers/shims, retainers | As measured | Final stack unresolved |
| Hubs/interfaces | 8 mm clamping hubs plus servo-to-shaft interfaces | 3 hubs, 2 drive interfaces | Exact compatible servo drive interface remains unresolved |
| Fasteners | M3/M4 bolts, nuts, washers, inserts | 1 set | Determine lengths from actual stacks; does not resolve servo-specific screws |
| Camera mounting | Existing webcam, straps/pad or verified tripod hardware | 1 | Camera is assumed owned; record mass, envelope, cable exit, and mounting interface |
| Wiring/protection | Rated wire, connectors, fuses, terminals, heat-shrink | 1 set | Breadboards/jumpers are logic-only; motor power requires rated wiring |
| Printed structure | Current V8 CAD/print package | 1 assembly | Fit coupons and delivered-part measurements precede final assembly |

## Materials discrepancy to resolve

The supplied parts sheet lists PETG filament, while the current V8 K1 Max print
handoff was prepared around Creality Hyper PLA assumptions. This repository does
not choose between them automatically. The printer/operator must select and
validate the actual material/profile before generating machine-specific G-code.

## Deferred items

Optical source, receiver electronics, independent permission circuitry, and any
related second controller are deferred until the camera, simulation, and
laser-free motion milestones pass. Development and calibration use a screen
reticle or LED dummy.

## Required measurements before hardware integration

- Servo case, ears, flange height, output-axis offset, spline, and supplied screws.
- Hub bore, bolt pattern, thickness, shaft lengths, collars, and bearing fits.
- Camera body/clip envelope, mass, field of view, cable exit, and mount.
- Board, connector, switch, and power-distribution envelopes.
- Joint zero/direction, travel limits, speed, deadband, backlash, and feedback noise.

## Source documents

- `reference/Laser_Turret_Parts.pdf` - original parts worksheet.
- `PROCUREMENT.md` - dated budget, supplier, and unresolved-interface review.
- `../cad/turret_v8_K1Max/reference/V5_PARTS_AUDIT.md` - prior mechanical/electrical audit.
- `../cad/turret_v8_K1Max/README.md` - current print and assembly assumptions.
