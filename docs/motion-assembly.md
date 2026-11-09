# Motion inspection assembly

Open `solid_3mm/Motion-3mm.SLDASM` in SolidWorks 2025, with the adjacent part files available. This separate assembly shares the 3 mm fabrication parts; it does not replace the fabrication assemblies or cutting files.

The frame, main axle, motor housing, and mounting screws are fixed. Both wheels, the internal ring gear, eight skewers, bearing envelopes, and bearing collars form one rigid rotor. The rotor has an unlocked concentric joint on the stationary axle plus an axial positioning mate. The pinion has its own unlocked axis and axial positioning mate.

The ring has 60 teeth (two seed teeth repeated 30 times), and the pinion has 25 teeth. The internal gear mate is set to 60:25, with the intended same direction of rotation. One wheel revolution corresponds to 2.4 pinion revolutions. The four existing cardboard gondolas have unlocked hanging joints. They can pivot manually; this is not a gravity or torque simulation. The motor and bearings are simplified envelopes; internal motor-shaft and bearing-race motion is not modelled separately.

## Inspection

1. Open the motion assembly and stay on the **Model** tab.
2. Use **Assembly > Move Component > Free Drag**, then drag a wheel rim or spoke away from the axle. Both wheels and the glued rotor parts should follow, and the small gear should turn at the stated ratio.
3. Drag a gondola body to swing it about its hanger.
4. Use the middle mouse button to orbit the view. Hide an obstructing component from its context menu to inspect the holder or gear engagement, then show it again.
5. Close without saving after experimenting if you want to retain the supplied assembly pose.

## Verification status

The saved assembly has 33 resolved components, 13 fixed frame/hardware components, 27 active mates, and no reported static mate errors. Its saved component transforms match the documented fabrication pose to numerical precision. No cutting geometry has changed.

**Interactive coupled dragging confirmed by the user on 5 November 2026:** both wheels and the small gear follow when dragging in SolidWorks. This confirms interactive wheel/pinion coupling; gondola swing and the exact angular ratio were not independently measured in that check.

Automated `SetTransformAndSolve3` and drag-operator tests did not propagate connected components, including in a separate minimal joint test and another session. This API limitation does not reflect the confirmed interactive behaviour. See `validation/motion-3mm.json` for the recorded status.

The native package includes this assembly and all its referenced parts. STEP files do not preserve SolidWorks mates.
