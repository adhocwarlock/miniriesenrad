# Electronics: lights, sound and motion

Status: hardware chosen and ordered (4 November 2026). Firmware not written yet.

For the overall plan, timeline and who does what, see [project-plan.md](project-plan.md).

This replaces the original electronics (Adafruit Metro ESP32-S2, two relays, 12 V). The old firmware in [`miniriesenrad/`](../miniriesenrad/) and [`media/wiring.PNG`](../media/wiring.PNG) belong to the upstream design and are kept only for reference. Do not follow the old wiring picture.

Contents:

1. [Concept](#1-concept)
2. [Behaviour](#2-behaviour)
3. [Parts list](#3-parts-list)
4. [Power](#4-power)
5. [Pin assignment](#5-pin-assignment)
6. [Complete wiring diagram](#6-complete-wiring-diagram)
7. [Wire list](#7-wire-list)
8. [Build steps, with a test after each](#8-build-steps)
9. [Box layout](#9-box-layout)
10. [Software setup](#10-software-setup)
11. [Setting the clock](#11-setting-the-clock)
12. [Songs](#12-songs)
13. [Firmware design](#13-firmware-design)
14. [Configuration options](#14-configuration-options)
15. [Safety](#15-safety)
16. [Troubleshooting](#16-troubleshooting)
17. [Maintenance and after Christmas](#17-maintenance-and-after-christmas)

---

## 1. Concept

The Ferris wheel stands on a cardboard box that is decorated as a small Christmas market town. Small house-shaped boxes stand around the wheel. Together with the gondolas they make the 24 calendar doors. All electronics sit inside the box.

| Function | How |
|---|---|
| Motion | An N20 gear motor drives the wheel through the laser-cut plywood gears, mounted in a plywood holder (see [3mm-revision.md](3mm-revision.md)). A relay switches it on and off. |
| Lights | 50 individually addressable LEDs (WS2811 pixels) poke through 12 mm holes in the lid, between the houses. |
| Sound | A 3 W speaker inside the box, driven by the amplifier on the controller board. One song per day, 1 to 24 December, played as **chiptunes** synthesised on the board by default. MP3s are optional. |
| Date | A DS3231 real-time clock with a coin cell keeps the real date while everything is switched off. |
| Controls | Three momentary push buttons and a rocker on/off switch, mounted in the lid. |

Design rules:
- As few parts, wires and solder joints as possible.
- Everything orderable on Amazon.de.
- Nothing electrical on the rotating wheel, so no slip ring is needed.

## 2. Behaviour

This is the planned behaviour. All times and brightness values are adjustable in `config.py` (see [section 14](#14-configuration-options)).

### Controls

| Control | Action |
|---|---|
| Rocker switch | Turns the whole calendar on or off, including the controller. |
| **Song** button, short press | Plays today's song with a matching light show. |
| **Song** button, during a song | Stops the song. |
| **Wheel** button | Turns the wheel for a set time, about one gondola step. A chime plays when it starts. Pressing again while it turns stops it. |
| **Lights** button | Cycles the light modes: warm twinkle → colour chase → rainbow → off → warm twinkle … |
| **Lights** button, held 5 s | Shows the current date as stored in the clock: the LEDs light up as many pixels as the day of the month, e.g. 7 for 7 December. Useful to check the clock. |

### Daily logic

| Date | Song button plays |
|---|---|
| Before 1 December | A preview jingle, so it can be tested and shown off early. |
| 1–24 December | Song number *DD* for that day. |
| 24 December | Finale: the day's song plus an extended light show and one full turn of the wheel. |
| 25 December onwards | A random song from all 24, so it keeps working over the holidays. |

### Idle behaviour

- **At switch-on:** a short start-up jingle plays and the lights fade in to the last selected mode.
- **After `IDLE_DIM_MINUTES` without a button press:** the lights dim to a low glow.
- **After `IDLE_OFF_MINUTES`:** the lights go dark. Any button press wakes them.
- **Wheel safety:** the motor never runs longer than `WHEEL_MAX_SECONDS` in one go, even if something goes wrong in the software.

## 3. Parts list

### Ordered

| # | Part | Product (Amazon.de) | Key data | Qty |
|---|---|---|---|---|
| 1 | Controller | Adafruit RP2040 Prop-Maker Feather, Adafruit product 5768 (€32.97) | RP2040, 8 MB flash, USB-C; built-in MAX98357 3 W I2S amplifier; screw terminals for NeoPixels, speaker and one button; 3-pin servo header; STEMMA QT I2C connector; LIS3DH accelerometer; 3.3 V regulator (500 mA peak) | 1 |
| 2 | Real-time clock | DS3231 RTC module with CR2032 coin cell | I2C address 0x68. The common "ZS-042" type also has an EEPROM at 0x57, which is unused here. | 1 |
| 3 | Relay | ARCELI 1-channel 3 V relay module, optocoupler, high-level trigger (5-pack, €8.99) | SRD-03VDC-SL-C relay, coil about 130 mA at 3.3 V; contacts 10 A; screw terminals NO / COM / NC | 1 (+4 spare) |
| 4 | Motor | JYUDAUFU GA12-N20 micro gear motor, 3–12 V, 35–140 rpm, metal gears (2-pack, €9.99) | 12 × 10 mm body, 3 mm D-shaft, datasheet in [`motor/`](../motor/). At 5 V roughly 1.5× its 3 V speed. | 1 (+1 spare) |
| 5 | LED string | ruimeimei WS2811 12 mm RGB pixel string, 50 pcs, **DC5V option** (€15.99) | 12 mm bullet pixels, 3-wire (5 V, data, GND), roughly 60 mA per pixel at full white | 1 |
| 6 | Speaker | QUARKZMAN 3 W 4 Ω mini speaker with JST PH2.0 lead (€5.69) | Matches the amplifier: 4–8 Ω, up to 3 W | 1 |
| 7 | Push buttons | Mowpiny 16 mm momentary push buttons, normally open, screw terminals (24 pcs, €7.49) | 3 A 250 V rating, far more than needed | 3 (+21 spare) |
| 8 | On/off switch | Mevvyla round rocker switch, SPST, 10 A, with wires (6 pcs, €5.99) | 2 pins, pre-wired | 1 (+5 spare) |
| 9 | Power input | QUARKZMAN USB-C female breakout board (3-pack, €5.99) | Needs 5.1 kΩ CC pull-downs, see [section 4](#4-power) | 1 (+2 spare) |
| 10 | Power supply | 65 W USB-C PD charger (already owned) | PD chargers default to 5 V; at least 3 A needed | 1 |

### Small parts and tools

| Part | Use | Notes |
|---|---|---|
| 1000 µF electrolytic capacitor, ≥6.3 V (10 V or 16 V is fine) | Across 5 V/GND at the LED string input | Polarised: the stripe marks minus |
| 1N4007 diodes, about 5 pcs | 1 across the motor (flyback); 1–2 in series to slow the motor if needed; 1 for the LED data fix in [section 16](#16-troubleshooting) | Stripe marks the cathode |
| 5.1 kΩ resistors, 2 pcs | CC pull-downs on the USB-C breakout, only if it lacks them | |
| 3 female–female jumper wires | Servo header → relay module | |
| Optional: STEMMA QT / Qwiic to female jumper cable (JST SH 1.0 mm, 4-pin) | Clock without soldering | Search "Qwiic Kabel Dupont". Colours: black GND, red 3.3 V, blue SDA, yellow SCL. |
| Red and black stranded wire, 0.5 mm² (about AWG 20) | 5 V and GND rails | About 2 m of each |
| Thin stranded wire, 0.14–0.25 mm² | Buttons, data line, clock | About 2 m, ideally several colours |
| Heat-shrink tubing assortment | Insulating every solder joint | |
| microSD card | **Not needed** for this board | |
| Tools | Soldering iron and solder, side cutter, wire stripper, multimeter, USB-C data cable (must carry data, not charge-only), small screwdriver for the screw terminals, hot-glue gun or foam tape | |

## 4. Power

### Architecture

Everything runs on 5 V from one USB-C charger, through one rocker switch.

```
USB-C PD charger (5 V, ≥3 A)
        │  USB-C cable
 USB-C breakout board ── CC1 ─[5.1 kΩ]─ GND
        │                CC2 ─[5.1 kΩ]─ GND   (only if not already on the board)
        │ VBUS (+5 V)                  GND
   [rocker switch]                       │
        │                                │
 +5 V rail ─┬─ LED string +5 V         GND rail ─┬─ LED string GND
            ├─ relay COM                         ├─ motor − (and flyback diode anode)
            ├─ Feather "USB" pin                 ├─ Feather "GND" pin
            └─ 1000 µF capacitor + ──────────────┴─ capacitor −  (at the LED string input)
```

- The **rails** are simply short thick wires soldered together, with heat-shrink over each joint. Alternatively, solder them onto a small piece of perfboard. No WAGO connectors are needed.
- The Feather is powered through its **USB** header pin. That pin is connected to the USB-C socket's 5 V, so the Feather behaves exactly as if it were plugged into a charger.

### Why a PD charger gives 5 V

USB-C PD chargers always start at 5 V. They only switch to 9, 15 or 20 V when the connected device negotiates a higher voltage. Nothing in this project negotiates, so the charger stays at 5 V, up to 3 A.

### The CC pull-down resistors

A USB-C charger only switches on its output when it detects a device. It detects it by a 5.1 kΩ resistor from each CC pin to ground.

1. Plug the charger into the breakout board. Measure between **VBUS** and **GND** with the multimeter.
2. **About 5 V:** the resistors are already on the board. Done.
3. **0 V:** unplug, then solder one 5.1 kΩ resistor from **CC1 to GND** and one from **CC2 to GND**. Measure again.

Never put a resistor directly across VBUS and GND: that is a pointless load and does not trigger the charger.

### Current budget

| Load | Typical | Peak | Note |
|---|---|---|---|
| Feather (RP2040) | 30 mA | 50 mA | |
| Amplifier and speaker | 100 mA | ~700 mA | Peaks on loud bass notes at full volume |
| Relay coil | 130 mA | 130 mA | From the Feather's 3.3 V regulator, so it counts on 5 V too |
| Motor | 100–200 mA | ~500 mA | Peak at start-up |
| LED string, 50 pixels | 200–600 mA | 1.2 A | Firmware limits brightness to `LED_MAX_BRIGHTNESS` = 0.4. Unlimited full white would be about 3 A. |
| **Total** | **~0.8 A** | **~2.6 A** | All peaks at the same moment are unlikely. A 3 A supply is enough. |

Feather 3.3 V regulator load: RP2040 (~50 mA), relay coil (~130 mA), clock (~1 mA), accelerometer (<1 mA). Together that is under 200 mA of the regulator's 500 mA peak rating.

### Why the LEDs and motor take power from the rail, not from the Feather

The Feather's own 5 V outputs (NeoPixel terminal **5V** and servo header **V+**) go through an on-board transistor switched by GPIO23. Adafruit gives no current rating for it. Only the LED **data** and **ground** go to the Feather's terminal. The terminal's 5V screw stays empty.

### ⚠️ The one rule

> **Switch the rocker OFF before plugging the Feather into a PC.**

The rail feeds the Feather's USB pin. With the rocker on and a PC cable plugged in, the charger and the PC would both drive the same 5 V line. With the rocker off, the PC powers the Feather alone. The LEDs, motor and relay don't work then, but songs and code can be copied safely.

## 5. Pin assignment

| Function | Feather connection | GPIO | CircuitPython name |
|---|---|---|---|
| LED string data | NeoPixel terminal **Neo** | 21 | `board.EXTERNAL_NEOPIXELS` |
| LED string ground | NeoPixel terminal **G** | – | – |
| Speaker + / − | Speaker terminal **+ / −** | I2S: DATA 16, BCLK 17, WS 18 | `board.I2S_DATA`, `board.I2S_BIT_CLOCK`, `board.I2S_WORD_SELECT` |
| **Lights** button | Button terminal **Btn** and **G** | 19 | `board.EXTERNAL_BUTTON` |
| **Song** button | Header **A0** and **GND** | 26 | `board.A0` |
| **Wheel** button | Header **A1** and **GND** | 27 | `board.A1` |
| Relay IN | Servo header **Sig** | 20 | `board.EXTERNAL_SERVO` |
| Relay GND | Servo header **G** | – | – |
| Relay VCC | Header **3V** | – | – |
| Clock SDA / SCL | **STEMMA QT** connector, or header **SDA / SCL** | 2 / 3 | `board.STEMMA_I2C()` / `board.I2C()` |
| Clock VCC / GND | STEMMA QT, or header **3V / GND** | – | – |
| 5 V in | Header **USB** | – | – |
| Ground in | Header **GND** | – | – |

### Used on the board: keep these free

| Pin | Used for |
|---|---|
| GPIO23 `EXTERNAL_POWER` | Enables the amplifier and the terminal/servo 5 V. The firmware sets it high at start. |
| D4 (GPIO4) | On-board status NeoPixel |
| D13 | Red on-board LED |
| GPIO22 | Accelerometer interrupt |
| GPIO7 | BOOT button |
| I2C 0x18 | LIS3DH accelerometer, which shares the bus with the clock at 0x68 without conflict |

### Spare pins for later

A2, A3, D5, D6, D9–D12, D24, D25, SCK, MOSI, MISO, RX, TX. Possible uses:
- A Hall sensor for exact gondola positions.
- A light sensor for automatic dimming.
- A motion sensor that wakes the calendar.
- More buttons.

### Relay power: 3V, never V+

The ARCELI relay is a 3 V type. Power its **VCC** from the Feather's **3V** header pin. The servo header's **V+** is 5 V and would overheat the coil.

The relay module has a small jumper. It sets **high-level trigger**, meaning the relay closes when IN goes high. That is also the safe direction: at power-up and during a reset, GPIO20 is low, so the motor stays off.

## 6. Complete wiring diagram

```
                                   ┌──────────────────────────────────────────┐
                                   │     Adafruit RP2040 Prop-Maker Feather   │
                                   │                                          │
 +5 V rail ───────────────────────►│ USB (header)         Neo  (terminal) ────┼──────► LED string DATA IN
 GND rail  ───────────────────────►│ GND (header)         G    (terminal) ────┼──────► LED string GND (also to GND rail)
                                   │                      5V   (terminal)  ✗  │        (leave empty)
 Song button ──── A0 ─────────────►│ A0                                       │
      └────────────── GND ────────►│ GND                  Btn  (terminal) ────┼──── Lights button ──┐
 Wheel button ─── A1 ─────────────►│ A1                   G    (terminal) ────┼─────────────────────┘
      └────────────── GND ────────►│ GND                                      │
                                   │                      Spk+ (terminal) ────┼──────► speaker red
 Relay VCC ◄──────────────────────│ 3V                   Spk− (terminal) ────┼──────► speaker black
                                   │                                          │
                                   │ Servo header:  Sig ──┼──────► Relay IN
                                   │                G   ──┼──────► Relay GND
                                   │                V+  ✗ │        (leave empty)
                                   │                                          │
 DS3231 ◄═════ STEMMA QT cable ════│ STEMMA QT  (or SDA/SCL/3V/GND header)    │
                                   └──────────────────────────────────────────┘

 Relay contacts:   +5 V rail ── COM          NO ──┬── motor +
                                                  │
                                       1N4007 ▲ stripe to motor +
                                                  │
                   GND rail ──────────────────────┴── motor −
```

## 7. Wire list

Measure the lengths on your own box. The values below are only starting points for a box of about 40 × 30 cm.

| # | From | To | Wire | Approx. length | Joint |
|---|---|---|---|---|---|
| W1 | USB-C breakout VBUS | Rocker pin 1 | red 0.5 mm² | 10 cm | solder |
| W2 | Rocker pin 2 | +5 V rail | red 0.5 mm² | 10 cm | solder |
| W3 | USB-C breakout GND | GND rail | black 0.5 mm² | 10 cm | solder |
| W4 | +5 V rail | Feather USB pin | red thin | 10 cm | solder |
| W5 | GND rail | Feather GND pin | black thin | 10 cm | solder |
| W6 | +5 V rail | LED string +5 V (input end) | red 0.5 mm² | as needed | solder |
| W7 | GND rail | LED string GND (input end) | black 0.5 mm² | as needed | solder |
| W8 | LED string DATA IN | Feather terminal **Neo** | any colour, thin | ≤30 cm if possible | solder / screw |
| W9 | LED string GND | Feather terminal **G** | black thin | ≤30 cm | solder / screw |
| C1 | 1000 µF capacitor | across W6/W7 at the LED string input, stripe to GND | – | – | solder |
| W10 | +5 V rail | Relay **COM** | red 0.5 mm² | 10 cm | screw |
| W11 | Relay **NO** | Motor + | red thin (motor lead) | to the motor | screw / solder |
| W12 | Motor − | GND rail | black thin (motor lead) | to the motor | solder |
| D1 | 1N4007 across the motor terminals | stripe to motor + | – | – | solder |
| W13 | Feather servo **Sig** | Relay **IN** | jumper F–F | 20 cm | plug |
| W14 | Feather servo **G** | Relay **GND** | jumper F–F | 20 cm | plug |
| W15 | Feather **3V** header | Relay **VCC** | thin, or jumper F–F | 20 cm | solder / plug |
| W16 | Song button terminal 1 | Feather **A0** | thin | to the lid | solder / screw |
| W17 | Song button terminal 2 | Feather **GND** | thin | to the lid | solder / screw |
| W18 | Wheel button terminal 1 | Feather **A1** | thin | to the lid | solder / screw |
| W19 | Wheel button terminal 2 | Feather **GND** | thin | to the lid | solder / screw |
| W20 | Lights button terminal 1 | Feather terminal **Btn** | thin | to the lid | screw |
| W21 | Lights button terminal 2 | Feather terminal **G** | thin | to the lid | screw |
| W22 | Speaker red | Feather terminal **Spk +** | speaker lead (plug cut off) | – | screw |
| W23 | Speaker black | Feather terminal **Spk −** | speaker lead | – | screw |
| W24 | Clock | Feather STEMMA QT, or SDA / SCL / 3V / GND | STEMMA QT cable or 4 thin wires | 10–20 cm | plug / solder |

**Several GND wires at the Feather:** the Feather has only a few GND header pins, and three wires need one (W5, W17, W19). Twist the two button grounds together before soldering, or join them to one short wire.

## 8. Build steps

Build and test one part at a time. If something fails, you then know exactly which step caused it.

### Step 1: Load the software first
Do this before soldering anything, with only the USB data cable connected. See [section 10](#10-software-setup).

- **Test:** the CIRCUITPY drive appears, and the on-board NeoPixel blinks or changes colour as the test firmware runs.

### Step 2: Power input
1. Check the USB-C breakout for 5 V, adding the CC resistors if needed (see [section 4](#4-power)).
2. Solder the breakout to the rocker switch, and build the +5 V and GND rails (W1–W3).
3. Heat-shrink every joint.

- **Test:** with the charger plugged in, measure 5 V between the rails with the rocker on, and 0 V with it off.

### Step 3: Power the Feather from the rail
1. Solder W4 (rail → USB pin) and W5 (rail → GND pin).

- **Test:** with the rocker **on** and **no PC cable** connected, the Feather starts. Its on-board LEDs light and the test firmware runs.

### Step 4: Speaker
1. Cut the white plug off the speaker lead and strip about 5 mm of each wire.
2. Screw red into **+** and black into **−**.

- **Test:** the start-up jingle plays. If it's too quiet or too loud, adjust `VOLUME` in `config.py`.

### Step 5: LED string
1. Find the input end of the string and identify the wires (see [section 16](#16-troubleshooting) if unsure).
2. Solder W6/W7 and the capacitor C1 at the input end.
3. Connect data (W8) to **Neo** and ground (W9) to **G**.

- **Test:** the idle animation runs along all 50 pixels.
- If the colours are wrong, for example red shows as green, change `LED_COLOR_ORDER` in the config. It's not a wiring fault.
- If the first pixel or the whole string flickers randomly, see [section 16](#16-troubleshooting).

### Step 6: Buttons
1. Connect the lights button to **Btn/G**.
2. Solder the song button to **A0/GND** and the wheel button to **A1/GND**.

- **Test:** each button does its job, and the serial console prints the button names when pressed (see [section 16](#16-troubleshooting) for how to open it).

### Step 7: Relay (without the motor yet)
1. Plug the 3 jumpers W13–W14 onto the servo header and the relay.
2. Connect relay VCC to the **3V** pin (W15).
3. Check that the relay's jumper is on **H** (high-level trigger).

- **Test:** pressing the wheel button makes the relay click and its LED light for `WHEEL_RUN_SECONDS`, then click off.

### Step 8: Motor
1. Solder the flyback diode D1 straight onto the motor terminals, stripe to the **+** terminal (the red wire). Then solder the motor leads.
2. Connect W10 (rail → COM), W11 (NO → motor +) and W12 (motor − → GND rail).

- **Test:** the motor turns while the relay is closed.
- **Wrong direction:** swap the two motor wires. Keep the diode stripe on whichever wire is now on NO.
- **Too fast:** add 1N4007 diodes in series between NO and motor +, stripe towards the motor. Each one drops about 0.7 V. Tuning `WHEEL_RUN_SECONDS` helps too.

### Step 9: Clock
1. Connect the DS3231 via the STEMMA QT cable, or solder 4 wires to **3V / GND / SDA / SCL**.
2. Insert the CR2032 coin cell.
3. Set the time (see [section 11](#11-setting-the-clock)).

- **Test:** switch off for a minute, then on again. Holding the lights button for 5 s shows the correct day of the month.

### Step 10: Move everything into the box
Mount the boards, then route and fix the wires (see [section 9](#9-box-layout)). Repeat all the tests after closing the box.

## 9. Box layout

### Holes in the lid

| Hole | Size | Tip |
|---|---|---|
| Push buttons | 16 mm | Drill or cut small and widen. Thin cardboard tears; glue a piece of thicker card or plywood under the lid as reinforcement. |
| Rocker switch | measure it, about 20 mm | Snap-in type: the hole must be tight, so reinforce it. |
| LED pixels | 12 mm | Push them through from below. A drop of hot glue holds them. |
| Speaker | a grid of 5–10 small holes (3–4 mm), or slots | Screw or glue the speaker under the lid by its lugs, facing up. |
| Motor wires | 3–5 mm | Next to the motor holder |

### Inside the box
- Mount the Feather and the relay on the box floor with foam tape or hot glue on their undersides. Keep the terminal screws reachable.
- Keep the Feather's **USB-C socket** reachable from outside, through a slot in the box wall. That way songs and firmware can be updated without opening the box.
- Keep the clock's **coin cell** reachable.
- Put the USB-C breakout board in the back wall, so the charger cable plugs in from outside.
- Fix the wires with tape or hot glue so they can't be pulled off the terminals.
- Keep the speaker cable away from the motor wires; it reduces interference noise.
- Leave a few ventilation holes. Nothing gets hot, but the relay coil and the Feather are warm to the touch.

### On top
- The wheel stand (feet and supports) is glued or slotted onto the lid. Mechanical details are Codex's area (see [project-plan.md](project-plan.md)).
- Plan the LED positions together with the houses, for example a few LEDs in front of each house as "windows", a row along a "market street", and a few around the foot of the wheel.

## 10. Software setup

### Install CircuitPython (once)
1. Download the latest stable CircuitPython `.uf2` file for **"Adafruit RP2040 Prop-Maker Feather"** from [circuitpython.org/downloads](https://circuitpython.org/downloads).
2. Connect the Feather to the PC with a USB-C **data** cable. The rocker must be off.
3. Hold the **BOOT** button, tap **RESET**, then release BOOT. A drive called **RPI-RP2** appears.
4. Drag the `.uf2` file onto RPI-RP2. The board restarts, and a drive called **CIRCUITPY** appears.

### Install the libraries
The firmware needs these libraries from the [Adafruit CircuitPython Bundle](https://circuitpython.org/libraries), matching the CircuitPython version:

| Library | For |
|---|---|
| `neopixel.mpy` | LED string |
| `adafruit_ds3231.mpy` | Clock |
| `adafruit_register/` | Needed by the clock driver |
| `adafruit_bus_device/` | Needed by the clock driver |
| `adafruit_debouncer.mpy` | Clean button presses |
| `adafruit_ticks.mpy` | Timing |
| `adafruit_led_animation/` | Light modes |
| `adafruit_lis3dh.mpy` | Optional: accelerometer, for knock-to-wake |

The modules for audio, MP3, synthesiser and I2S are built into CircuitPython: `audiobusio`, `audiomp3`, `audiomixer`, `synthio`.

The easiest way is to copy the `firmware/` folder from this repository: it will contain the right `lib/` folder. Alternatively, use the `circup` tool (`pip install circup`, then `circup install neopixel adafruit_ds3231 …`).

### Copy the firmware
1. Rocker off, Feather connected to the PC.
2. Copy `code.py`, `config.py` and the `lib/`, `songs/` and `chiptunes/` folders onto CIRCUITPY.
3. The board restarts automatically after each file change.
4. Eject the drive safely before unplugging.

## 11. Setting the clock

The DS3231 is set once. After that it runs on its coin cell for years, about ±2 minutes per year.

Planned procedure:
1. Connect the Feather to the PC (rocker off).
2. Create a file `settime.txt` on CIRCUITPY containing the current date and time plus about 30 seconds, for example:
   ```
   2026-11-20 18:30:00
   ```
3. Unplug and restart the board. At start-up the firmware reads the file and sets the clock. It then stores a marker in the RP2040's non-volatile memory so the same file isn't applied again on every restart.
4. Delete `settime.txt` the next time the board is connected.

Alternatively, the clock can be set from the serial console with one command.

The clock doesn't handle daylight saving time. That doesn't matter for an advent calendar, because only the date is used.

## 12. Songs

### Storage
The Feather has 8 MB flash. About 6.5 MB is free for songs after CircuitPython, the firmware and the libraries.

| Format | Size | 24 songs |
|---|---|---|
| MP3, 32 kbps mono | 4 KB per second | about 65 s each |
| MP3, 64 kbps mono | 8 KB per second | about 34 s each |
| Chiptune (synthesised) | a few KB per song | full length, any number |

**Chiptunes are the default.** MP3s are an optional extra for single days. Both can be mixed.

### Song plan
Fill in this table and keep it outside the repository, or commit it without copyrighted file names if you prefer.

| Day | Song | Format |
|---|---|---|
| 1 | … | chiptune (default) / MP3 |
| … | … | … |
| 24 | finale | … |

### Preparing an MP3 in Audacity (free)
1. Open the bought MP3 or CD track in Audacity.
2. Select the part you want, about 60 seconds, and delete the rest. A good choice is the chorus.
3. Add a 1–2 second fade-out at the end: select the end, then Effect → Fading → Fade Out.
4. Tracks menu → Mix → **Mix Stereo Down to Mono**.
5. Set the project rate (bottom left) to **22050 Hz**.
6. Effect → Volume and Compression → **Normalize** to −1 dB, so all songs play at the same volume.
7. File → Export → Export as MP3. Choose **Constant bitrate, 32 kbps**, mono.
8. Name the file with two digits: `01.mp3`, `02.mp3` … `24.mp3`. Also add `00.mp3` for the preview jingle and `start.mp3` for the start-up sound.

Copy the files into the `songs/` folder on CIRCUITPY.

### Chiptunes (default)
Chiptunes are synthesised on the board with CircuitPython's `synthio`: square, triangle, sawtooth and noise waveforms, with several voices for melody, bass and drums. Each song is a small Python file in `chiptunes/` (`01.py` … `24.py`), so it plays at full length and the lights follow every note.

Three ways to get a chiptune:
1. **Public-domain carols:** Claude arranges them directly. These may be committed to the repository.
2. **Your own MIDI file:** a PC script, `tools/midi2chip.py` (planned), converts a MIDI file you own into a chiptune file. Use this for copyrighted songs. Put the result in `chiptunes/private/`, which is never committed.
3. **Original tunes:** Claude writes new melodies, e.g. in the style of 90s Christmas pop with bells and a shuffle beat.

If `songs/DD.mp3` exists for a day, it replaces that day's chiptune. A file in `chiptunes/private/DD.py` replaces `chiptunes/DD.py`.

### Copyright
- Playing bought music privately at home is fine, and so is giving a private copy to a close person.
- Don't use songs from streaming subscriptions, because they're copy-protected.
- **Never commit copyrighted songs, or chiptune arrangements of them, to this public repository.**
- `songs/` and `chiptunes/private/` will be excluded through `.gitignore`. Arrangements of traditional public-domain carols (Jingle Bells, O Tannenbaum, Stille Nacht, Kling Glöckchen, Deck the Halls, …) may be committed.

## 13. Firmware design

Written by Claude, in CircuitPython. The code goes in `firmware/` in this repository.

### Files

```
firmware/
├── code.py          main loop, starts everything
├── config.py        all user-adjustable settings (section 14)
├── hardware.py      pin setup, external power enable, relay, buttons, clock
├── lights.py        light modes and light shows
├── audio.py         amplifier, MP3 playback, mixer, volume
├── chiptune.py      small synthesiser player for the chiptune files
├── calendar.py      date logic: which song today, preview, finale, after Christmas
├── lib/             CircuitPython libraries (section 10)
├── chiptunes/       01.py … 24.py: public-domain arrangements and original tunes (in Git)
│   └── private/     arrangements made from your own MIDI files (never in Git)
└── songs/           optional MP3s: 00.mp3 … 24.mp3, start.mp3 (never in Git)
tools/
└── midi2chip.py     PC script: MIDI file → chiptune file (planned)
```

### Structure
- **One non-blocking main loop:** no `time.sleep()` while anything is happening. Buttons, lights, audio and motor all update in each pass, so lights keep animating during music and buttons always respond.
- **States:** `IDLE`, `PLAYING`, `WHEEL_TURNING`, `SHOW_DATE`, `DIMMED`, `OFF`.
- **Buttons** are debounced. Short and long presses are told apart.
- **Light-to-music sync:** chiptunes trigger LED effects directly on each note. MP3s use a pattern per song, timed to the music's tempo (`SONG_BPM` in the song table), or a generic sparkle if no tempo is given.
- **Watchdog:** the RP2040's hardware watchdog restarts the board if the code ever hangs. The relay pin is low after any reset, so the motor stops.
- **Error display:** problems are shown in colour on the on-board status NeoPixel:
  - red blink: clock not found,
  - yellow blink: song file missing.

  Errors are also printed to the serial console. The calendar keeps working as well as it can; for example, without a clock it falls back to a day counter stored in flash.

### Start-up sequence
1. Enable external power (GPIO23 high) and make sure the relay is off.
2. Read the clock. Apply `settime.txt` if present and new.
3. Restore the last light mode from non-volatile memory.
4. Play `start.mp3` and fade in the lights.
5. Enter the main loop.

## 14. Configuration options

Planned contents of `config.py`. Change values with any text editor directly on CIRCUITPY; the board restarts with the new settings.

| Setting | Default | Meaning |
|---|---|---|
| `WHEEL_RUN_SECONDS` | 3.0 | Motor run time per wheel button press. Tune until one press moves one gondola step. |
| `WHEEL_MAX_SECONDS` | 15.0 | Hard safety limit for one motor run |
| `WHEEL_FULL_TURN_SECONDS` | 25.0 | Run time for one full turn, used in the finale |
| `VOLUME` | 0.6 | 0.0–1.0 |
| `LED_COUNT` | 50 | Number of pixels |
| `LED_COLOR_ORDER` | `"RGB"` | `"RGB"` or `"GRB"`, depending on the string batch |
| `LED_MAX_BRIGHTNESS` | 0.4 | Hard limit; keeps the current under ~1.2 A |
| `LED_IDLE_BRIGHTNESS` | 0.25 | Normal brightness |
| `IDLE_DIM_MINUTES` | 10 | Dim after this long without a button press |
| `IDLE_OFF_MINUTES` | 30 | Lights off after this long |
| `DEFAULT_LIGHT_MODE` | `"twinkle"` | Mode at first start |
| `PREVIEW_BEFORE_DECEMBER` | `True` | Song button plays `00.mp3` before 1 December |
| `AFTER_CHRISTMAS` | `"random"` | `"random"`, `"24"` (repeat the finale) or `"off"` |
| `SONGS` | table | Per day: title, file, tempo (BPM), light pattern |

## 15. Safety

- **Low voltage only.** Everything runs on 5 V from a certified charger. No mains wiring inside the box. The relay and switches are rated for mains, but they are **only** used at 5 V here.
- **Short circuits:** heat-shrink every joint. A short on the 5 V rail makes the charger cut out; it won't burn, but it stops everything. Check with the multimeter (step 2 of [section 8](#8-build-steps)) before the first power-up.
- **Cardboard and heat:** nothing in the box gets hot during normal use. Still:
  - don't cover the charger itself;
  - keep the relay and Feather from being buried in decoration or cotton "snow";
  - leave a few ventilation holes;
  - switch off with the rocker at night or when leaving the room. That's also the normal way to use it.
- **Motor:** limited by `WHEEL_MAX_SECONDS` and the watchdog, so it can't keep running if a gondola jams.
- **Coin cell:** keep spare CR2032 cells away from small children and pets. Swallowed coin cells are dangerous.
- **PC rule:** rocker off before connecting the USB cable to a PC (see [section 4](#4-power)).

## 16. Troubleshooting

### Serial console
The firmware prints status messages: date, button presses, songs played, errors. To see them:
1. Connect the Feather to the PC (rocker off).
2. Open a serial monitor on the Feather's COM port at 115200 baud. Options: the Mu editor, the VS Code serial monitor, or PuTTY.
3. Press Ctrl+D in the console to restart the code and watch the start-up messages.

### Common problems

| Problem | Likely cause | Fix |
|---|---|---|
| Nothing happens at all, rocker on | USB-C breakout gives no 5 V | Measure VBUS; add the 5.1 kΩ CC resistors ([section 4](#4-power)) |
| Feather works from the PC but not from the charger | W4/W5 not connected or swapped | Check the USB and GND header joints |
| No sound | External power not enabled, speaker wires loose, or file missing | Check the serial console; tighten the terminals; check the file names (`01.mp3`, not `1.mp3`) |
| Sound distorts or the board restarts at loud parts | Volume too high, or supply sagging | Lower `VOLUME`; check the charger gives 3 A; check the rail wires are 0.5 mm² |
| Songs stutter | MP3 bitrate or sample rate too high | Re-export at 32 kbps, mono, 22050 Hz |
| No LEDs light | Wrong end of the string, or data not connected | Use the input end (arrows point away from it); check Neo and G |
| LEDs show the wrong colours | Colour order | Change `LED_COLOR_ORDER` |
| First LED flickers, or random colours | The 3.3 V data signal is weak for 5 V pixels | 1) Keep the data wire short, under 30 cm. 2) "Diode trick": feed the **first pixel only** through a 1N4007 diode from +5 V (stripe towards the pixel). It then runs at ~4.3 V, its input accepts 3.3 V, and it passes a clean 5 V signal on to the rest. 3) A 330 Ω resistor in the data line. |
| LEDs dim and turn orange towards the end of the string | Voltage drop on the thin string wires | Lower `LED_MAX_BRIGHTNESS`, or also connect +5 V/GND to the far end of the string |
| Relay doesn't click | Relay VCC on the wrong pin, or trigger jumper wrong | VCC must go to **3V**; the jumper must be on **H** |
| Relay clicks but the motor doesn't turn | COM/NO swapped, or motor wiring | Wire COM to +5 V and NO to the motor; check with the multimeter |
| Motor turns the wrong way | Polarity | Swap the motor wires and move the diode accordingly |
| Wheel too fast or jerky | 5 V on a 3 V-speed motor | Series diodes ([section 8](#8-build-steps), step 8); shorter `WHEEL_RUN_SECONDS` |
| Board restarts when the motor starts | Start-up current dip or interference | Check the flyback diode is in place and the right way round; keep the motor wires short and away from the data wire |
| Wrong song or wrong day | Clock not set, or coin cell empty or missing | Hold the lights button for 5 s to check the day; set the time again ([section 11](#11-setting-the-clock)); replace the CR2032 |
| Status LED blinks red | Clock not found | Check the STEMMA QT cable or the SDA/SCL wires; 3V and GND |
| CIRCUITPY drive missing | Charge-only USB cable, or the board is in bootloader mode | Use a data cable; press RESET once |
| CIRCUITPY drive is full | Songs too large | Use 32 kbps mono, or shorten the songs |

## 17. Maintenance and after Christmas

- **Coin cell:** lasts years. Replace it if the date is lost after switching off.
- **Next year:** set the clock again if needed (daylight saving doesn't matter), swap songs on CIRCUITPY, and the calendar is ready for 1 December 2027.
- **Spare parts** from the multi-packs: 4 relays, 1 motor, 21 buttons, 5 rocker switches, 2 USB-C boards. Keep a spare motor and relay with the calendar.
- **Updating the firmware:** pull the latest `firmware/` from this repository and copy it onto CIRCUITPY. Keep `songs/` and `config.py` if you've customised them.
