# Project plan: Ferris wheel advent calendar

Plan date: 4 November 2026. Deadline: the calendar must be running on **1 December 2026**.

Contents:

1. [Goal](#1-goal)
2. [Who does what](#2-who-does-what)
3. [File ownership](#3-file-ownership)
4. [Interfaces between mechanics and electronics](#4-interfaces-between-mechanics-and-electronics)
5. [Brief for Codex (copy and paste)](#5-brief-for-codex)
6. [Brief for Claude (copy and paste)](#6-brief-for-claude)
7. [How changes are handed over](#7-how-changes-are-handed-over)
8. [Hardware summary](#8-hardware-summary)
9. [Decisions and why](#9-decisions-and-why)
10. [Timeline](#10-timeline)
11. [Risks](#11-risks)
12. [Open questions](#12-open-questions)

---

## 1. Goal

A motorised Ferris wheel advent calendar, given as a Christmas gift and standing in the recipient's bedroom for December. It is based on [kn0del/miniriesenrad](https://github.com/kn0del/miniriesenrad) (original design credit: kn0del) and built from laser-cut 3.0 mm plywood (standard recorded in `AGENTS.md`).

- **Scene:** the wheel stands on a cardboard box decorated as a small **Christmas market town**. The wheel carries a few gondola boxes (Folia 9388 type, 80 × 73 × 55 mm). Small **house boxes** stand around it. Together they form the 24 calendar doors.
- **Motion:** a button press makes the motor turn the wheel by about one gondola.
- **Lights:** 50 addressable LEDs poke through holes in the box lid between the houses. They have several modes and light shows synchronised to the songs.
- **Sound:** one song per day, 1–24 December, from a speaker inside the box. The songs are **chiptunes** synthesised on the board (default), with optional MP3s for single days.
- **Date:** a real-time clock knows the date, so the right song plays every day.
- **Hidden electronics:** everything is inside the box. Three buttons and an on/off switch are in the lid. Everything runs from one USB-C charger.

The detailed electronics description is in [electronics.md](electronics.md). The mechanical revision is in [3mm-revision.md](3mm-revision.md).

## 2. Who does what

The work is split between the builder and two AI assistants. **Each assistant stays in its own area and does not edit the other's files.** Anything that crosses the boundary goes through the builder (see [section 7](#7-how-changes-are-handed-over)).

### Builder (repository owner)

| Area | Tasks |
|---|---|
| Decisions | Final say on design, parts, songs and schedule |
| Purchasing | All parts, Amazon.de only |
| Mechanical fabrication | Laser cutting 3.0 mm plywood (with kerf test first), cutting the skewers, gluing and assembling the wheel, gears and plywood motor holder |
| Electrical build | Soldering and wiring following [electronics.md](electronics.md), step by step with the tests |
| Scene | Cardboard box, lid layout, houses, gondolas, decoration, drilling the holes |
| Music | Choosing songs; buying MP3s; trimming and exporting in Audacity |
| Testing | Running the tests and reporting results, photos and serial console output to the assistants |
| Git | All commits and pushes; keeping copyrighted songs out of the repository |

### Codex: mechanics

| Area | Tasks |
|---|---|
| CAD | SolidWorks parts and assemblies in [`solid_3mm/`](../solid_3mm/) (current); [`solid/`](../solid/) is a superseded reference set |
| Laser cutting | DXF outlines in [`lasercutter/`](../lasercutter/) |
| Construction standard | [`AGENTS.md`](../AGENTS.md) and [`design/materials.json`](../design/materials.json): 3.0 mm plywood for every custom part. Gears, pinion and the five-piece motor holder are laser-cut. The old STLs in [`3d_print/`](../3d_print/) are upstream reference only. |
| Exchange formats | STEP export in [`exports/`](../exports/) |
| Verification | CAD and DXF checks in [`validation/`](../validation/) |
| Documentation | [3mm-revision.md](3mm-revision.md) and further mechanical docs; assembly images in [`media/`](../media/) |
| Interfaces | Motor mount for the GA12-N20; gear ratio; fixing the wheel stand on the box; wire exit for the motor; optional magnet/sensor positions ([section 4](#4-interfaces-between-mechanics-and-electronics)) |

**Codex does not** write or change firmware, wiring or electronics documentation.

### Claude: electronics and firmware

| Area | Tasks |
|---|---|
| Electronics concept | Part selection and checking listings before purchase |
| Power and wiring | Power architecture, current budget, pin assignment, wiring diagram, wire list: [electronics.md](electronics.md) |
| Firmware | CircuitPython firmware in a new [`firmware/`](../firmware/) folder: buttons, relay/motor timing, LEDs, audio, clock, calendar logic, safety |
| Light design | Light modes, per-song light shows, music synchronisation |
| Music software | Song schedule; chiptune player (default); MIDI-to-chiptune converter for the builder's own MIDI files; chiptune arrangements of public-domain carols and original tunes; optional MP3 playback |
| Support | Help with the electrical tests, debugging from serial console output and photos |

**Claude does not** edit SolidWorks, DXF, STL or STEP files, the validation data, or the mechanical docs.

## 3. File ownership

| Path | Owner | Notes |
|---|---|---|
| `solid_3mm/` | Codex | Current SolidWorks 2025 native files |
| `solid/` | Codex | Superseded reference set |
| `design/`, `AGENTS.md` | Codex | Construction standard and materials |
| `lasercutter/` | Codex | DXF, mm, 1:1 |
| `3d_print/` | Codex | Upstream STLs, reference only |
| `exports/` | Codex | STEP |
| `validation/` | Codex | CAD and DXF measurements |
| `docs/3mm-revision.md` | Codex | Mechanical revision notes |
| `media/assembly-*.png` | Codex | CAD renders |
| `motor/` | Builder | Motor datasheet; read by both |
| `docs/electronics.md` | Claude | Electronics description |
| `firmware/` | Claude | New CircuitPython firmware (to be created) |
| `media/wiring*.png` | Claude | New wiring diagram, when made; the old `media/wiring.PNG` is upstream and kept for reference |
| `miniriesenrad/` | Upstream | Original PlatformIO firmware for the Metro ESP32-S2. Kept for reference, not used. |
| `docs/project-plan.md` | Shared | This file: either assistant may update its own sections and its rows in the tables |
| `README.md` | Shared | Small additive edits only; tell the builder |
| `.gitignore` | Shared | Small additive edits only; tell the builder |
| `LICENSE` | Upstream | Do not change |

## 4. Interfaces between mechanics and electronics

These are the points where the two areas meet. A change on one side may need a change on the other, so they are agreed through the builder.

| # | Interface | Mechanics side (Codex) | Electronics side (Claude) | Status |
|---|---|---|---|---|
| I1 | **Motor** | Done by Codex: five-piece 3 mm plywood holder on the drive leg; motor fixed with 2 × M1.6 × 5 screws; laser-cut pinion with a 3 mm D-bore. Datasheet in [`motor/`](../motor/). The builder needs to buy the M1.6 × 5 screws. | Drives it at 5 V through a relay. On/off only: no speed control, no reverse, no soft start. | **Fixed.** Motor already bought. |
| I2 | **Wheel speed** | Internal ring 60 teeth, main pinion 25 teeth: wheel rpm = measured motor-output rpm / 2.4; same direction. Actual loaded rpm at 5 V still needs measurement. See [motion assembly](motion-assembly.md). | `WHEEL_RUN_SECONDS` in `config.py` | Tune in testing. Electronics can slow the motor with series diodes. |
| I3 | **Gondola step** | Eight hanger positions at 45 degrees; current CAD shows four cardboard gondolas. Final populated positions are the builder's choice. | Wheel button run time ≈ step angle ÷ wheel speed | Open |
| I4 | **Start-up jerk** | Gondolas swing when the motor starts at full speed. Pivots that move freely help. | No soft start possible with a relay | Accept; check during the loaded test |
| I5 | **Motor wires** | The rear holder plate has a wiring opening. Still open: the route from there down to the box lid, and a 3–5 mm hole in the lid | Two wires: + to relay NO, − to GND, with a flyback diode at the motor | Open |
| I6 | **Wheel stand on the box** | How the feet are fixed to the lid: glue, slots or screws; the footprint on the lid | Nothing electrical on the wheel or stand except the motor | Open |
| I7 | **No electrics on the rotating wheel** | – | All LEDs are on the stationary lid, so no slip ring is needed | Decided |
| I8 | **Lid layout** | Footprint of the feet and wheel; clearance under the wheel | Holes: 3 × 16 mm buttons, ~20 mm rocker, 50 × 12 mm LEDs, speaker grid | The builder lays out the lid |
| I9 | **Optional position sensor** | Space for small neodymium magnets on the wheel, one per gondola, and a Hall sensor mount at the bottom | A Hall sensor on a spare GPIO; firmware stops the wheel exactly at each gondola | Not planned now; possible later |
| I10 | **Motor load** | Friction of the bearing, gear backlash, gondola weight | The relay switches up to 10 A; the motor draws ~0.1–0.5 A | Builder confirmed the motor is strong enough |

## 5. Brief for Codex

Copy and paste this to Codex:

> You are responsible for the **mechanical part** of this project: a motorised laser-cut Ferris wheel advent calendar (fork of kn0del/miniriesenrad). Your area is SolidWorks (`solid_3mm/`, with `solid/` as reference), laser DXFs (`lasercutter/`), the construction standard (`AGENTS.md`, `design/`), legacy STLs (`3d_print/`), STEP exports (`exports/`), validation data (`validation/`) and the mechanical docs (`docs/3mm-revision.md`, CAD renders in `media/`).
>
> Do **not** edit firmware (`firmware/`, `miniriesenrad/`) or the electronics docs (`docs/electronics.md`). Another assistant (Claude) does electronics and firmware. Coordinate through the builder; the shared plan is in `docs/project-plan.md`. You may update your own rows and sections there.
>
> Electronics facts you need:
> - The motor is a **GA12-N20 micro gear motor, 3–12 V**: 12 × 10 mm body, 3 mm D-shaft, datasheet in `motor/`. It is fixed and already bought.
> - It runs at **5 V** (faster than at 3 V) and is switched **on/off by a relay**: no soft start, no speed control, no reverse.
> - Nothing electrical is on the rotating wheel. The motor wires need a route down into the cardboard base box through a 3–5 mm hole near the motor holder.
>
> Please provide:
> 1. The gear ratio and expected wheel rpm at 5 V.
> 2. The number of gondolas and the angle per step.
> 3. How the wheel stand fixes to the cardboard lid, with its footprint.
> 4. The motor wire exit position.
> 5. Optionally, mounting positions for one magnet per gondola and a Hall sensor at the bottom, for exact stopping later.

## 6. Brief for Claude

Copy and paste this to start a new Claude session:

> You are responsible for **electronics and firmware** of this project. Read `docs/project-plan.md` and `docs/electronics.md` first. Your area is `docs/electronics.md`, `firmware/` and the new wiring diagrams. Do not edit CAD, DXF, STL, STEP or validation files, or `docs/3mm-revision.md`: Codex handles mechanics. Hardware is a Feather RP2040 Prop-Maker with CircuitPython, a DS3231, a relay-switched N20 motor, a 50-pixel WS2811 string and a 3 W speaker. Keep copyrighted songs out of the repository.

## 7. How changes are handed over

1. **An assistant needs something from the other side.** It writes the request in its answer to the builder, or adds it to [Open questions](#12-open-questions). It does not edit the other side's files.
2. **The builder passes it on.** Copy the request to the other assistant, or point it at the open question.
3. **The other side answers** in its own files, or updates its rows in [section 4](#4-interfaces-between-mechanics-and-electronics).
4. **Commits:**
   - The builder commits.
   - Prefer separate commits for mechanics and electronics, e.g. `mech: …` and `elec: …` / `fw: …` prefixes.
   - Work happens on `develop`. Merge to `main` when a version works.
5. **Never in Git:** copyrighted MP3s, chiptune arrangements of copyrighted songs, WiFi passwords, SolidWorks lock files (`~$*`, already ignored).

## 8. Hardware summary

Full details, wiring and part data are in [electronics.md](electronics.md).

| Part | Choice | Role |
|---|---|---|
| Controller | Adafruit RP2040 Prop-Maker Feather | Brain; 3 W amplifier, LED terminal, button terminal, servo header, STEMMA QT, 8 MB flash, CircuitPython |
| Clock | DS3231 RTC with CR2032 | Real date without WiFi |
| Motor switch | ARCELI 1-channel 3 V relay, high-level trigger | Motor on/off |
| Motor | JYUDAUFU GA12-N20, 3–12 V, at 5 V | Turns the wheel |
| Lights | ruimeimei WS2811 12 mm pixel string, 50 pcs, 5 V | Scene lighting |
| Sound | QUARKZMAN 3 W 4 Ω speaker | Songs and effects |
| Controls | 3 × Mowpiny 16 mm momentary buttons (song, wheel, lights); Mevvyla rocker switch | User input, main switch |
| Power | 65 W USB-C PD charger at 5 V; QUARKZMAN USB-C breakout with 5.1 kΩ CC pull-downs | One supply for everything |

## 9. Decisions and why

| Decision | Alternatives considered | Reason |
|---|---|---|
| Prop-Maker Feather | Original Metro ESP32-S2 with add-on boards | Amplifier, speaker terminal and LED terminal built in: one board instead of four, far less wiring |
| | Raspberry Pi | Linux boot takes 20–40 s; the SD card can be corrupted by switching off with the rocker; no amplifier; a Pi 5 needs 5 A |
| | Raspberry Pi Pico | Same chip as the Feather, but no amplifier or terminals |
| | Arduino UNO R4 WiFi + DFPlayer | WiFi and full-length songs, but needs an extra MP3 module |
| | ESP32-A1S Audio Kit | Full songs and WiFi, but pins are tight, versions vary, and the software is more fiddly |
| | ACEBOTT ESP32 Max | Easy plug-in pins, but no audio at all |
| DS3231 clock | WiFi time; a day counter | No WiFi on the Feather; a counter can be fooled by extra button presses. The clock always knows the real date. |
| One relay, 3 V type, powered from 3V | A motor driver (DRV8833), or a 5 V relay | Simplest no-solder-ish switching; the 3 V relay was already found. Powered from the 3V pin because the servo V+ is 5 V. |
| Motor at 5 V | Separate 3 V supply | Motor is rated 3–12 V; one supply for everything; series diodes can slow it |
| LEDs on the lid, none on the wheel | LEDs on the wheel | No slip ring or battery on the rotating part |
| WS2811 pixel string | Plain fairy lights with a MOSFET | Every LED is controllable, and the bullet pixels push into 12 mm holes |
| Songs: chiptunes by default, optional MP3s | Full songs from an SD card; MP3s only | Builder's choice. Chiptunes fit at full length in a few KB each, and the lights can follow every note. 8 MB flash ≈ 1 minute per MP3. No extra module. |
| One USB-C supply, one rocker | Two cables (Feather separate) | One switch turns everything off |
| Soldered joints, no WAGO | WAGO lever connectors | Builder is fine with some soldering |
| All parts from Amazon.de | Specialist shops | One order, fast delivery |

## 10. Timeline

| When | What | Who |
|---|---|---|
| 4 Nov | Plan, part selection, orders | Builder, Claude |
| 4 Nov onwards | 3.0 mm plywood revision, wider wheel, laser-cut gears and N20 motor holder (done); gear ratio and stand-on-box details | Codex |
| ~5–7 Nov | Parts arrive. CircuitPython installed and tested on the bare Feather ([electronics.md step 1](electronics.md#8-build-steps)). | Builder |
| ~5–12 Nov | Laser kerf test; cut wheels, feet, supports, gears and motor holder; assemble the wheel | Builder, Codex |
| by ~12 Nov | First firmware: buttons, relay timing, LED modes, MP3 playback, clock, calendar logic | Claude |
| ~12–20 Nov | Electrical build steps 2–9 with tests; tune the wheel step, brightness and volume | Builder, Claude |
| ~15–25 Nov | Choose and prepare songs; chiptune arrangements; per-song light shows | Builder, Claude |
| ~20–28 Nov | Cardboard box, lid layout and holes, houses, decoration; final assembly (step 10) | Builder |
| 29–30 Nov | Full test run: set the clock, simulate several days, loaded wheel rotation, test after switching off overnight | Builder, Claude |
| **1 Dec** | Day 1 | 🎄 |

**Buffer:** the last week has slack for re-cuts, a faulty part or re-ordering from Amazon (next-day Prime delivery).

## 11. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Laser kerf or sheet thickness differs from nominal | Slots and skewer holes too tight or loose | Kerf test piece first (see the mechanical docs) |
| Gondolas snag on the frame or swing at motor start | Wheel jams | Loaded rotation test; free pivots; `WHEEL_MAX_SECONDS` stops the motor |
| Motor too fast at 5 V | Gondolas swing, imprecise step | Series diodes; shorter run time; gear ratio |
| Wheel step drifts, since timing alone can't stop at an exact position | Gondola not exactly at the bottom | Accept, or add the Hall sensor later (I9) |
| 3.3 V data too weak for the 5 V pixels | LED flicker | Diode trick or short data wire ([electronics.md](electronics.md#16-troubleshooting)) |
| USB-C breakout without CC resistors | No power | Measure; solder 2 × 5.1 kΩ |
| MP3 stutter on the RP2040 | Bad sound | 32 kbps mono 22 kHz; fall back to chiptunes |
| Clock not set or coin cell empty | Wrong song | Date check by holding the lights button; set via `settime.txt` |
| A faulty part | Delay | Spares from the multi-packs; Amazon next-day re-order |
| Copyrighted songs end up in the public repo | Legal trouble | `.gitignore` for `songs/`; check before each push |
| The two assistants edit the same files | Conflicts, lost work | File ownership ([section 3](#3-file-ownership)); handover via the builder |

## 12. Open questions

| # | Question | Who answers | Status |
|---|---|---|---|
| Q1 | How many gondolas, and which days are gondolas and which are houses? | Builder, Codex | Open |
| Q2 | Gear ratio and wheel rpm at 5 V | Codex | Ratio documented: 60:25, wheel rpm = motor rpm / 2.4. Loaded 5 V speed still to measure. |
| Q3 | How the stand fixes to the box lid, and its footprint | Codex | Open |
| Q4 | Motor wire exit position | Codex | Open |
| Q5 | Box size and lid layout: buttons, rocker, LEDs, speaker | Builder | Open |
| Q6 | Song for each day (chiptune by default; which ones from own MIDI files) | Builder | Open |
| Q7 | Wheel run time per press | Builder, Claude, in testing | Open |
| Q8 | Light mode wishes (colours, effects, a special one for the 24th) | Builder | Open |
