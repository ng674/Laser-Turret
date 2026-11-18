# Laser turret V8 — Creality K1 Max filament handoff

This is the COMPLETE nominal printed assembly: 14 pieces, arranged into TWO batches. Send the single ZIP. Do not also print previous V6/V7 files or the resin support drafts.

## Printer and material

Target: Creality K1 Max, stock 300 x 300 x 300 mm bed, assumed stock 0.4 mm nozzle. User described filament as "hyper hla"; interpreted as Creality Hyper PLA, NOT resin. Confirm that interpretation with the operator. If the bed is reduced by a modification, check fit again.

## The two jobs

Print PRINT_BATCHES/group_01.3mf ONCE and PRINT_BATCHES/group_02.3mf ONCE. The two STLs with the same names are fallback geometry for other slicers, NOT additional jobs. All duplicate parts are already included.

Batch 1: flat electronics panel (1), one-piece foundation (1), leg (1).
Batch 2: servo mounting deck/base (1), camera pad (1), camera post (1), carrier (1), leg (1), switch cradle (1), head (1), horn spacer (2), tray foot (2).

If a piece is already successfully printed, omit just that named object from the 3MF. Do not print the individual backup STLs as well.

## Required operator step before printing

The 3MFs contain named positioned objects plus PrusaSlicer process settings for removable snug supports, brim and infill. They were imported in PrusaSlicer 2.9.5 and reference-sliced there. They are NOT calibrated K1 Max machine profiles or printer-ready G-code. Select the operator's real K1 Max/nozzle and Hyper PLA profiles, preserve the layout and scale, and verify the process/support settings before slicing. Start/end machine code was deliberately left blank in the layout profile to prevent treating it as ready-to-run machine instructions. Do not export print G-code from that layout-only machine profile.

In Creality Print, Prusa-specific process settings may not transfer. Import the fallback grouped STL, split into objects without rearranging, select K1 Max + actual Hyper PLA, and set conventional removable supports for all overhangs, including internal bridges. Use normal/snug supports with an interface, or the operator's calibrated equivalent. Verify layer preview, support reach and brim clearance. Save the completed Creality Print project so repeats require no further setup.

Reference process (not physical qualification): 0.24 mm layer height; 0.20 mm first layer; four walls; 20% gyroid infill; five top/bottom layers; 5 mm brim; automatic snug supports; 45 degree threshold; supports allowed on model as well as bed; 0.24 mm top/bottom support separation; 0.4 mm XY separation; two interface layers. The model-to-support air gap creates the intended removable interface. Do not fuse support structures into the permanent CAD. PLA reference temperatures are 220 C nozzle and 45 C bed, based on Creality's published Hyper PLA starting settings; use the actual filament/bed profile where it differs. These gaps may need adjustment for the operator's actual profile. Remove supports BEFORE assembly. Clip in small sections and deburr mating surfaces; don't wrench against a thin bracket.

## Electronics panel fix

The former raised side rails have been removed. The new 200 x 130 x 4 mm panel is completely flat underneath, with only through holes/slots and no raised edges. Print its broad flat face on the bed. This removes the troublesome raised-side geometry and preserves the existing mounting positions and cable-tie slots. The reported symptom alone does not establish whether the old failure also involved adhesion, extrusion or cooling; geometry cannot correct those machine/process problems.

The larger K1 Max also accommodates the 230 x 100 mm foundation as one piece, replacing the resin-bed split. Existing screw locations remain; no seam hardware is required.

## What is included

PRINT_BATCHES: two editable 3MF projects, two fallback grouped STLs, two OpenSCAD layout previews.
CAD: editable OpenSCAD assembly source. Open main.scad, press F5 for preview.
INDIVIDUAL_BACKUPS: each nominal part as STL for replacement prints. Quantities above take precedence.
OPTIONAL_FIT_PARTS: alternative spacer cores/shims and fit coupons. These are NOT extra required assembly pieces and are not in the nominal batches.
VALIDATION: mesh/clearance reports and reference slicer logs.

Existing servo interface assumptions remain provisional: the printed horn holes are clearance holes, not confirmation of the metal horn thread. Check delivered screws and engagement before tightening. Nominal spacers are 6.8 mm. No printer-specific first-print success or physical servo fit has been demonstrated.

## Standard sharing workflow and sources

OpenSCAD is the editable geometry source; STL/3MF transfers the mesh; a native slicer project preserves print preparation; machine-specific G-code is generated only after matching printer and material profiles. Multiple small objects can share one plate/project. One file per tiny part is unnecessary.

Creality identifies K1 Max as an FDM filament printer with a 300 mm cube volume:
https://store.creality.com/blogs/all/creality-k1-vs-k1-max
Creality's published Hyper PLA starting parameters:
https://store.creality.com/blogs/all/k1-k1-max-printing-parameter-settings
Prusa support settings and contact separation:
https://help.prusa3d.com/article/support-material_1698
OpenSCAD exports:
https://files.openscad.org/documentation/manual/Using_OpenSCAD_in_a_command_line_environment.html
