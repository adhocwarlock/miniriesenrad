# Project construction standard

Use **3.0 mm plywood for every custom laser-cut part**, including the wheels, legs, braces, gears, motor holder, bearing-support collars, and any new sheet parts. This is the user's current standard; do not revert to the earlier 3.5 mm or upstream 4 mm designs unless the user changes it.

Current native CAD is in `solid_3mm/`. The root `solid/` folder is a superseded/reference set. Keep current models, cut lists, DXFs, STEP exports, and validation reports consistent.

Hardware and reference objects are exceptions:

- Gondola hangers: nominal 3 mm bamboo skewers.
- Main axle: nominal 10 mm round dowel; cut length follows the assembly.
- Purchased bearings: 10 mm bore × 15 mm outside diameter × 4 mm width, quantity two.
- Purchased N20 motor and metal fasteners.
- Cardboard gondolas, represented approximately in CAD.

Preserve the requested 72 mm clear distance between the inner faces of the two main wheels. Size bearing seats for the actual 15 mm outside diameter, not the upstream 14 mm opening. Check native rebuild/mate errors, sheet thickness, static interference, DXF units and closed contours after geometry changes. Keep current fabrication files and documentation consistent with the 3 mm standard; legacy upstream STL files are not the current build instructions.
