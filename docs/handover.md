# Maintainer handover

Prepared 9 November 2026 for publishing the local work to `adhocwarlock/miniriesenrad`, branch `develop`, at the owner's request. Original project and design credit: [kn0del/miniriesenrad](https://github.com/kn0del/miniriesenrad). Upstream history and the original [AGPL-3.0 license](../LICENSE) are retained.

## Mechanical build

Use **3.0 mm plywood for every custom sheet part**. Current files are in `solid_3mm/`; `solid/` contains superseded intermediate/reference CAD, including the earlier 3.5 mm tree holder. Do not mix the two fabrication sets.

- Main assembly: `solid_3mm/Assem1.SLDASM`; alternate pinion: `Assem1 - Copy.SLDASM`.
- Interactive inspection: `solid_3mm/Motion-3mm.SLDASM`. The owner confirmed on 5 November that both wheels and the small gear follow when dragging. Gondola swing and the exact angular ratio were not independently measured in that check.
- Wheels: 303.64 mm diameter, 72 mm clear gap, eight hanger positions at 45 degrees. Four cardboard gondolas are represented in CAD; final populated positions remain a build decision.
- Hardware: eight nominal 3 x 83 mm bamboo skewers, a nominal 10 x 99 mm main axle, two purchased 10 x 15 x 4 mm 100Cr6 bearings, and the purchased GA12/N20 motor. Skewers are glued into wheel holes, with gondolas free to pivot.
- Fifteen plywood pieces form the main build, including laser-cut gears, a five-piece tree-shaped motor holder, and two bearing collars. See the [cut list and assembly notes](3mm-revision.md).
- Internal gears: 60-tooth ring and 25-tooth main pinion, same direction; wheel speed is motor-output speed divided by 2.4. Measure loaded motor speed at the intended voltage before setting run time.
- Fabrication downloads: `exports/lasercut-3mm.zip`, `exports/native-3mm.zip`, and `exports/miniriesenrad-3mm.step`. STEP does not preserve SolidWorks mates.

Validation reports in `validation/` record resolved native references, 3 mm sheet thickness, feature/mate checks, zero static interferences in the fabrication assemblies, closed millimetre DXF contours, sheet volume versus cut area, and a STEP re-import with 33 valid solids. The motion assembly has 33 resolved components and 27 active mates. API drag tests did not propagate mates; the owner's interactive check is recorded separately. These are CAD checks, not loaded physical validation.

## Claude's additions

The [electronics description](electronics.md) and [shared project plan](project-plan.md) are included as authored, with mechanical interface rows updated for the established gear ratio and hanger positions. They describe the proposed Prop-Maker Feather RP2040, DS3231 clock, relay-switched motor, stationary LEDs, speaker, buttons, and calendar behaviour.

The PC tools `tools/chiptune_preview.py` and `tools/midi2chip.py` are included. The first needs `numpy`; the converter also needs `mido`. They generate preview WAVs on a computer. They are not device firmware.

There is currently **no new `firmware/` implementation** in this checkout. The nested `miniriesenrad/` directory is kn0del's original PlatformIO firmware and is retained for reference. Planned CircuitPython files mentioned in the electronics documentation still need to be created by Claude.

## Remaining work and ownership

- Builder: test-cut a joint and bearing seat for actual plywood thickness and laser kerf; assemble and test a full loaded rotation, clearances, free gondola pivots, shaft fit, and motor-screw engagement.
- Mechanics/Codex: settle stand attachment and footprint on the cardboard lid, and the motor-wire route into the box. Confirm physical motor dimensions against the supplied drawing before cutting.
- Electronics/Claude: implement and test CircuitPython firmware and wiring on the actual hardware. Measure loaded motor speed and tune run time per press. The gear ratio alone does not establish wheel rpm at 5 V.
- Builder: decide which hanger positions are populated, the house/gondola split across 24 days, lid layout, and song schedule.

Keep mechanical changes in `solid_3mm/`, `lasercutter/`, `design/`, `validation/`, and the mechanical notes. Claude owns electronics documentation, new firmware, and music tools. Coordinate interface changes through the owner using [project-plan.md](project-plan.md). The owner explicitly authorized this commit/push of both areas; future edits should continue to respect that ownership.

## Publication checks

On 9 November 2026: JSON parsing and Python syntax checks passed; both ZIP archives passed CRC checks; packaged native CAD matched the saved files. All three bundled demo arrangements rendered as 22050 Hz mono WAVs, and conversion of a newly generated one-note MIDI passed. Test audio was generated outside the repository and removed afterward. No device firmware or electrical hardware tests were performed in this publication step.

SolidWorks lock files, Python caches, local environment files, and the documented private song folders are ignored. Keep private song inputs and generated audio outside the repository. The CAD automation scripts use this workstation's SolidWorks installation and connection helper; paths need adaptation on another machine. The scripts refuse to replace an existing motion assembly.

Continue work on `develop`. Promote to `main` after review and the relevant physical/device checks; publishing these files does not certify an assembled toy or the planned electronics.
