# Procurement plan — 26 October 2026

This is a planning bill of materials, not an ordered or checkout-verified cart. The user's $300–$350 maximum supersedes the handoff's older $350–$400 allowance. Existing computer, webcam, and printer cost $0 here. Conservatively assume all three missing bench tools must be purchased. Original Downloads files remain unchanged.

## Recommendation and limits

Use DFRobot SER0044 feedback servos rather than the handoff's FEETECH FS5115M-FB pair. The manufacturer lists metal gears, RC PWM control, 0–3.3 V analog feedback, 4.8–7.2 V operation, and a 25T/5.80 spline. DigiKey lists $15.90 each and stock, with a possible US tariff. This is a cost-driven substitution, not evidence of equivalent accuracy. Restrict actual travel mechanically and in software; 270° capability is not the desired operating range.

A complete hardware planning subtotal is $298.21. With $85 for tools, $30 for estimated tax, $25 shipping/tariffs allowance, and $15 contingency, plan approximately $453.21. Unknown checkout costs, final mechanical interfaces, and optical modulation compatibility mean this is not a guaranteed completion price. A full $350 build is not established.

To stay under $350 now, build only the laser-free motion/vision prototype. Its planning subtotal is $203.70. Add $85 tools, $25 estimated tax, $20 shipping/tariffs allowance, and $15 contingency: $348.70. These are spending targets; if checkout exceeds them, defer nonessential purchases. This milestone supports mechanical tests, camera calibration, and motion logging. It does not complete laser-spot training data collection or the independent optical receiver.

## Complete project bill of materials

Prices marked allowance are estimates requiring supplier/cart confirmation. Exact shaft lengths, spline fit, mounting patterns, switch models, and source control interface remain to be resolved before purchasing those interface-dependent parts.

| Item | Quantity | Extended USD | Evidence / buying status |
|---|---:|---:|---|
| DFRobot DSS-M15S with analog feedback, SER0044 | 2 | 31.80 | Listed $15.90 each; available DigiKey listing; possible tariff |
| Raspberry Pi Pico H, SC0917 | 2 | 10.00 | Listed $5 each; one motion, one receiver; USB suffices, Wi-Fi unnecessary |
| Adafruit 1466 enclosed regulated 5 V, 4 A supply | 1 | 14.95 | Listed in stock; suitable initial selection for SER0044, validate transient voltage under actual load |
| 608ZZ bearings, 8 mm ID × 22 mm OD × 7 mm | 4 | 8.00 | Allowance; two pan, one each tilt side |
| Ground 8 mm steel round shaft stock | Enough for 1 pan + 2 tilt stubs | 10.00 | Allowance; lengths determined from the final adapter stack; avoid threaded rod |
| 8 mm collars, metal shims/spacers, bearing retainers | Approximately 4–6 collars plus spacers | 10.00 | Economy-hardware allowance; branded collars can exceed this |
| ServoCity 1309-0016-0008 Sonic clamping hubs | 3 | 23.97 | Listed $7.99 each; round 8 mm bore; confirm drawing before CAD |
| Metal servo-to-shaft drive interfaces | 2 | 19.98 | Allowance, NOT selected compatible SKUs; verify spline diameter/profile and 8 mm ROUND shaft interface before ordering |
| M3/M4 bolts, nuts, washers, inserts; metal angle brackets/stops; camera attachment | 1 set | 15.00 | Allowance; final lengths/counts follow mechanical layout; camera tripod screw only if webcam supports it |
| PETG filament | 1 kg | 20.00 | Allowance for purchased spool, not just consumed grams |
| Power distribution and prototyping materials | 1 set | 18.00 | Allowance: rated DC input connector, main/branch fuses and holders, 18–20 AWG feed, signal wire, terminals, heat-shrink, breadboard, perfboard, headers, LEDs/resistors, bulk capacitor and local decoupling |
| Full source-permission controls | 1 set | 35.00 | Allowance: four NC travel switches, access switch, NC stop, manual arm/reset, LTC6993-1 one-shot, latch/logic, normally-off high-side switch, adapters and passives; schematic-dependent, not a qualified ready-made assembly |
| USB data cables/adapters | 2 plus webcam provision | 12.00 | Allowance; match actual Mac ports, allow target cable length; extra hub may be necessary and is not assumed owned |
| Receiver electronics | 1 set | 26.02 | Four BPW34 at $1.37 = $5.48; MCP3204-CI/P listed $1.72; OPA4323IPWR listed $2.82; $16 allowance for reference/feedback buffers, adapters, soldered boards and passives |
| Printed marker target, diffuser and opaque matte lane/backstop material | 1 set | 10.00 | Allowance, compact bench enclosure using inexpensive sheet material; printing supports is covered by filament |
| Quarton VLM-650-01 LPO source, integrated driver/optics | 1 | 33.49 | Conditional candidate only; DigiKey regional USD listing; stock inconsistent across regional snapshots; confirm US cart and permitted switching/modulation with manufacturer |
| **Hardware subtotal** | | **298.21** | Conditional optical-source selection and several unquoted hardware groups |

### Optical-source qualification

Quarton identifies the exact **VLM-650-01 LPO** as Class 1, under 0.39 mW, with integrated optics/APC driver. LPT and LPA are different classes and are not substitutions. The manufacturer gives Ø10.5 × 19 mm; a distributor uses 10.4 mm, so physical measurement controls CAD. Its metal housing is at positive supply potential; do not casually bond it to ground.

The published two-wire interface does not establish a TTL input or suitability for the handoff's encoded pulses. Obtain confirmation of permitted supply switching, modulation rate/duty cycle, startup behavior, and documentation for the exact variant before buying. If incompatible, obtain a quote for a documented Class 1 FLEXPOINT configuration with supported modulation. The $33.49 line is then replaced by that quote. No supplier contact has been sent.

Use only an LED dummy during the first build. The full permission circuit remains a later design and test task. Buying a timer and switches does not qualify the circuit or the finished apparatus.

## Tool reserve

Reserve **$85** for an adjustable soldering iron, proper stand, solder/flux/cleaning materials, low-voltage electronics multimeter with probes/battery, metal digital calipers, and basic small hand tools. Buy only what is missing. Example listed iron: Adafruit 3685, $19.95. A CEN-TECH 59410 meter is listed around $25–$30 across current Harbor Freight pages; confirm checkout. A budget metal caliper is an allowance, not a verified product selection; prefer 0.01 mm display resolution and stated accuracy suitable for checking fit coupons. Display resolution is not measurement accuracy. A scope is not included: borrow access for receiver/gate waveform validation before qualifying optical operation.

## What to purchase first under the hard cap

The $203.70 laser-free parts plan uses the complete BOM above with these changes:

- One Pico H instead of two: save $5.
- No source yet: save $33.49.
- No receiver electronics yet: save $26.02.
- One-controller USB allowance $7 instead of $12: save $5.
- LED-stage switch/stop/dummy allowance $10 instead of full emission-control allowance $35: save $25. No laser is installed at this milestone.

Then $203.70 + $85 tools + $25 estimated tax + $20 shipping/tariffs + $15 contingency = **$348.70**.

The deferred items add $94.51 before their own fees and any price changes. This is a milestone within the budget, not a claim that the complete project costs $350. Borrowing tools or using existing filament reduces the eventual total; it does not resolve optical-source compatibility.

Order tools, two SER0044 servos, one Pico H, supply, and bearings first. Confirm metal drive adapters and shaft/hub stack against drawings before ordering shafts to length or final torque-path parts. The three hubs have an exact model, but the matching servo drive interfaces do not yet. Avoid REX-bore couplers on round shaft stock. Do not order generic 25T parts solely on tooth count.

## Gate before CAD release

Record servo case and mounting-ear dimensions, flange height, output-axis offset and spline details; hub bolt pattern and thickness; actual bearing/shaft dimensions; webcam mass, body envelope, cable exit and mounting interface; connector and board envelopes. The existing OpenSCAD dimensions remain provisional and have not been compiled or validated during this purchasing review. Final source mounting waits for the qualified source. Print fit coupons before full components.

## Sources checked

- [DFRobot SER0044 specification](https://www.dfrobot.com/product-1709.html)
- [DigiKey SER0044 price/stock](https://www.digikey.com/en/products/detail/dfrobot/SER0044/8827825)
- [Pico H $5 listing](https://www.canakit.com/raspberry-pi-pico.html)
- [Adafruit 1466 supply](https://www.adafruit.com/product/1466)
- [ServoCity round 8 mm Sonic hub](https://www.servocity.com/1309-series-sonic-hub-8mm-bore/)
- [DigiKey BPW34](https://www.digikey.com/en/products/detail/vishay-semiconductor-opto-division/BPW34/1681149)
- [Newark MCP3204-CI/P](https://www.newark.com/microchip/mcp3204-ci-p/adc-12bit-100ksps/dp/97K4491)
- [Mouser OPA4323IPWR](https://www.mouser.com/en/ProductDetail/Texas-Instruments/OPA4323IPWR?qs=ST9lo4GX8V06UEViuao2Jg%3D%3D)
- [Analog Devices LTC6993 variants](https://www.analog.com/en/products/ltc6993-1.html)
- [Quarton exact variant specification](https://www.quarton.com/industrial-red-dot-laser-module-vlm-650-01-series.html)
- [DigiKey source USD listing, regional snapshot](https://www.digikey.com.br/en/products/detail/quarton-inc/VLM-650-01-LPO/27346467)
- [FLEXPOINT quote alternative](https://www.lasercomponents.com/en/product/flexpoint-dot-laser-modules/)
- [Adafruit 3685 iron](https://www.adafruit.com/product/3685)
- [Harbor Freight meter](https://www.harborfreight.com/9-function-digital-multimeter-with-audible-continuity-59410.html)
