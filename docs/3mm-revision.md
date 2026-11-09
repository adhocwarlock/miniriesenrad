# Current build: 3 mm plywood

Revision date: 4 November 2026. Original project and design: [kn0del/miniriesenrad](https://github.com/kn0del/miniriesenrad), source `master` at `cafe75f`. Original history and license are retained. This revision supersedes the earlier 3.5 mm adaptation.

## Material and hardware standard

Every custom sheet part is **3.0 mm plywood**. The cardboard gondolas and purchased/round hardware are exceptions: N20 motor, metal fasteners, 3 mm bamboo skewers, 10 mm main axle dowel, and two purchased **10 bore × 15 outside × 4 wide mm, 100Cr6 steel bearings**. This requirement is recorded in `AGENTS.md` and `design/materials.json`.

Dimensions below are millimetres. Clearance slots normally allow 0.1 mm over the mating tab. Kerf compensation remains a separate CAM setting. Measure the sheet and test a joint and bearing seat before cutting the full set.

| Dimension | Current build |
| --- | ---: |
| Plywood thickness | 3.0 |
| Wheel diameter | 303.6374, unchanged |
| Clear gap between inner wheel faces | 72.0 |
| Outside-to-outside wheel width | 78.0 |
| Bamboo skewers | 3 diameter × 83 long, quantity 8 |
| Skewer holes | 3.2 diameter |
| Main axle dowel | 10 diameter × 99 long |
| Main axle openings in legs | 10.1 diameter |
| Bearings | 10 × 15 × 4, quantity 2 |
| Wheel and collar bearing seats | 15.1 diameter |
| Bearing collars | 24 outside × 15.1 inside × 3 thick, quantity 2 |
| Base support brace | 109.1 long × 12.5 high |
| Brace slots / inner-edge spacing | 3.1 / 92.9 |
| Leg slots accepting braces | 3.1 |

## Motor and plywood tree holder

The motor envelope follows the [supplied drawing](../motor/61cDM3ChHQL._SL1200_.jpg), supplied for the [GA12/N20 listing](https://www.amazon.de/dp/B0DPKYCZ97). The model uses a 10 × 12 gearbox face, 9 mm gearbox, 15 mm motor can, 1.2 mm rear cap, 10 mm shaft projection, and 2.5 mm terminal projection. The shaft is 3 mm diameter with 2.5 mm across the flat. Two M1.6 face threads are 9 mm apart, with 2.1 mm stated depth.

Internals and actual threads are omitted. The 4 mm front bushing uses a nominal 0.7 mm projection as an envelope assumption, not a separately specified boss dimension. Screw heads and terminals are simplified. See `motor/n20-mount-design.json` for all dimensions used.

The holder is five plywood pieces: front and rear tree plates, two identical side panels, and a cross-brace. Tabs engage 3.1 mm slots. Side-panel notches straddle the 3 mm drive leg and locate on the lower edge of its existing opening. Overall frame width is 17.7 mm through the leg's 17.9 mm opening. Glue the plywood joints while maintaining motor/pinion alignment.

The motor screws to the front plate, through a 4.4 mm bushing opening and two 1.8 mm screw-clearance holes. Two M1.6 × 5 screws nominally engage the motor by 2 mm through the 3 mm sheet. Check actual screw engagement against the 2.1 mm thread depth; do not bottom them in the gearbox. The rear plate has a wiring opening.

The original gear tooth profiles are preserved and extruded to 3 mm. The existing pinion already has a matching 3 mm D-shaped bore with 2.5 mm across the flat. Shaft engagement is 2.5 mm through the 3 mm pinion, with 0.5 mm shaft-tip clearance from the adjacent wheel face. This is a static motor envelope and assembly, not an internal gearbox or torque simulation.

## Bearings and main axle

The upstream 14 mm wheel opening is enlarged for the actual 15 mm bearing outside diameter. Glue a 3 mm support collar to each wheel's inner face. The combined wheel/collar housing is 6 mm long, supporting the complete 4 mm bearing width without a milled pocket or nonstandard sheet.

The 15.1 mm seats are clearance fits. Secure the outer race in the wooden housing while keeping adhesive off the inner race, shields/seals, and running surfaces. Use the main axle for alignment without bonding the rotating outer race to it. Actual dowel size and bearing fit need a physical check.

The axle stays a 10 mm round dowel, cut to 99 mm. The legs finish with 10.1 mm axle bores. A final clearance-bore feature preserves their original construction sketches and silhouette.

## Assembly coordinates

X is the main shaft direction.

| Component | X range |
| --- | --- |
| First / second wheel | 0–3 / 75–78 |
| First / second bearing | 0–4 / 74–78 |
| First / second bearing collar | 3–6 / 72–75 |
| Opposite / drive leg | −5 to −2 / 91–94 |
| Main axle | −5 to 94 |
| Gondola skewers | −1 to 82 |
| Ring gear and pinion | 78–81 |
| Front motor plate | 85.5–88.5 |
| Motor shaft | 78.5–88.5 |
| Motor body / terminal limit | 88.5–113.7 / 116.2 |
| Rear tree plate | 119–122 |

Skewers project 1 mm on the first-wheel side and 4 mm on the drive side. Keep glue beads small at the first end, which has 1 mm clearance to the nearby leg. Glue skewers at the wheel holes while leaving gondolas free to pivot. The 24 mm bearing collars occupy only the central hub region.

Representative gondolas are 55 mm deep along the shaft, with 10 mm clearance to the first wheel and 7 mm to the second. Their CAD hanger bores clear the 3 mm skewers. Cardboard envelopes are approximate: four gondolas are modeled, with no flexible folds or strings. The [Folia 9388 manufacturer](https://www.folia.de/en/advent-calendar-kit-village-in-the-snow-113-parts/9388) lists the real gondolas as 80 × 73 × 55 mm.

## Laser cut list

Cut **fifteen plywood pieces** for the main assembly, plus optional fences. Import these individual DXFs at **1:1 scale in millimetres**. They are not a nested sheet layout.

| File in `lasercutter/` | Quantity | Part |
| --- | ---: | --- |
| `wheeel.DXF` | 2 | Main wheels |
| `feet.DXF` | 2 | Legs |
| `support.DXF` | 2 | Base braces |
| `gear0.DXF` | 1 | Ring gear |
| `21.DXF` | 1 | Main pinion |
| `tree_front_3mm.DXF` | 1 | Front tree plate |
| `tree_rear_3mm.DXF` | 1 | Rear tree plate |
| `tree_side_3mm.DXF` | 2 | Side panels / leg locators |
| `tree_brace_3mm.DXF` | 1 | Holder cross-brace |
| `bearing_collar_3mm.DXF` | 2 | Bearing support collars |
| `fence.DXF` | Optional | Decorative fences |
| `gear1.DXF` | Alternative | Replaces `21.DXF` in the alternate assembly |

Do not use `stift.DXF` or the old STL files for this build. They are upstream alternatives/reference files; the current gondola hangers are bamboo skewers.

## Current files and verification

Current native files are in `solid_3mm/`: `Assem1.SLDASM` is the main assembly, and `Assem1 - Copy.SLDASM` keeps the alternate pinion. The portable assembly is `exports/miniriesenrad-3mm.step`. The root `solid/` folder is a superseded/reference set.

Verification covers valid solids, constant 3 mm sheet sections, resolved part references, feature/mate errors, measured clearances, and static interference. DXF audits check millimetre units, closed contours, duplicate edges, self-intersections, and cut area. Sheet volume is independently checked against DXF area × 3 mm. The STEP is re-imported to check all 33 solids.

Results are recorded in `validation/cad-3mm.json`, `validation/native-cad-3mm.json`, `validation/lasercut-3mm.json`, and `validation/interference-3mm.json`. Static geometry does not verify motor torque, deformation, kerf, or flexible cardboard snagging. Check a complete loaded rotation on the physical build.
