# Combined Smart Sensor and Actuator Development Plan for Sensors and Actuators Class

## Objective
Build and demonstrate a fluid control system using a 6-inch PVC end cap tank suspended by a 1/2-inch PVC pipe tripod, with water level detection via three CPX capacitive touch sensors using alligator clips, a voting system for reliability, and a 3D-printed tube-pinch valve controlled by a TowerPro SG92R servo to prevent overflow. Smart features are to be determined (TBD).

## Project Overview
- **Setup**: A 6-inch Schedule 40 PVC end cap (~711-1184 mL, ~1.5-2.5 inch depth) as the tank, suspended 6-12 inches above a lower container (e.g., 500-1000 mL cup) via a tripod made of 1/2-inch PVC pipes. Water flows through a 1/4-inch tube, controlled by a servo-driven 3D-printed pinch valve.
- **Challenge 1 (Fluid Level Sensor)**: Use CPX capacitive touch pads (A1-A3) with alligator clips to detect water level in the lower container.
- **Challenge 2 (Voting Sensor System)**: Implement three capacitive sensors (alligator clips) with majority voting (≥2 sensors detect water) for robust detection.
- **Challenge 3 (Smart Actuator System)**: Use an SG92R servo to close a 3D-printed pinch valve when the voting system triggers, stopping water flow.
- **Smart Features**: TBD.
- **Materials**:
  - **Tank**: 6-inch Schedule 40 PVC end cap.
  - **Tripod**: Three 2.5-foot 1/2-inch Schedule 40 PVC pipes, one 3/4-inch PVC tee, zip ties.
  - **Valve**: 1/4-inch aquarium tubing, SG92R servo (from CPX kit), 3D-printed pinch mechanism (PLA).
  - **Sensors**: Three alligator clips (from CPX kit) for capacitive probes, electrical tape/heat-shrink for insulation.
  - **Other**: Silicone sealant, jumper wires (from CPX kit).
- **Toolset**: CircuitPython on CPX (Mu editor), drill, hacksaw, 3D printer (school/library).
- **Deliverable**: Working prototype, CircuitPython code, demo video/report addressing all challenges, and analysis of system performance.

## Development Plan

### Step 1: Build Fluid Level Sensor (Challenge 1, 2-3 Days)
- **Task**: Create a single capacitive water level sensor.
  - Attach an alligator clip to CPX pad A1, with the metal jaw positioned in the lower container.
  - Insulate clip jaw partially with electrical tape, leaving ~0.5 cm² exposed for water contact.
  - Program in CircuitPython: Use `touchio.TouchIn` to read capacitance, set threshold (~1000, adjust via testing) for water detection.
  - Test: Submerge clip in water; use CPX NeoPixels and serial output for feedback.
- **Milestone**: Code detecting water level reliably, logged via serial monitor.

### Step 2: Implement Voting Sensor System (Challenge 2, 3-4 Days)
- **Task**: Expand to three capacitive sensors for voting.
  - Attach alligator clips to CPX pads A1-A3, placed at similar heights in the lower container for redundancy.
  - Insulate each clip’s jaw to prevent shorting; secure to container with tape/3D-printed holder.
  - Program voting logic: If ≥2 clips exceed threshold, set “level reached” flag.
  - Test faults: Disconnect one clip to ensure voting ignores it.
- **Milestone**: Code and hardware triggering “level reached” via majority vote, with NeoPixel feedback.

### Step 3: Build and Integrate 3D-Printed Pinch Valve (Challenge 3, 3-4 Days)
- **Task**: Construct tank and valve, integrate with sensors.
  - **Tank Setup**:
    - Drill 1/4-inch hole in side of 6-inch PVC end cap (~0.5 inches from bottom).
    - Attach 1/4-inch aquarium tubing with silicone sealant (cure 24 hours).
    - Drill two 1/8-inch holes in cap’s rim (above waterline) for zip tie suspension.
  - **Tripod**:
    - Cut three 2.5-foot 1/2-inch PVC pipes; join in 3/4-inch tee (friction fit or tape).
    - Suspend end cap from tee with zip ties, ~6-12 inches above lower container.
  - **Pinch Valve**:
    - 3D-print a bracket (30x20x5 mm, with 2 mm holes for SG92R screws) and pinch arm (20-30 mm, slots for servo horn and tube) in PLA (Tinkercad or Thingiverse ID 4530241, modified).
    - Mount SG92R on end cap near outlet (glue/screws); attach arm to servo horn.
    - Route tubing through arm’s slot; servo rotates to 90° to pinch tube shut.
    - Wire SG92R: signal to A6, power to VOUT, ground to GND.
  - **Program**: When voting flag is true, set `servo.angle = 90` to close valve; reset to 0° via CPX button (e.g., button_a).
- **Milestone**: Prototype where sensors trigger servo to pinch tube, stopping flow.

### Step 4: Test and Validate System (2-3 Days)
- **Task**: Run end-to-end tests.
  - Scenarios: Normal fill (valve closes on detection), single sensor fault (voting handles it), low/high water starts.
  - Measure: Detection accuracy (>95%), response time (<1s), voting reliability.
  - Visualize: Use NeoPixels for status; log data via serial.
  - Debug: Adjust sensor thresholds, reinforce 3D-printed arm if needed.
- **Milestone**: Demo video showing system preventing overflow in multiple trials.

### Step 5: Analyze, Optimize, and Document (2-3 Days)
- **Task**: Evaluate and refine.
  - Analyze: Voting effectiveness, servo reliability, system performance.
  - Optimize: Tune threshold, adjust 3D print for tighter pinch.
  - Document: Report with diagrams, code, results, and challenge alignment.
  - Presentation: 5-7 min demo with prototype video.
- **Milestone**: Final report and presentation slides.

## Timeline
- **Total Duration**: 12-17 days.
- **Week 1**: Steps 1-2 (Sensors and voting).
- **Week 2**: Steps 3-4 (Valve, tripod, testing).
- **Week 3 (if needed)**: Step 5 (Analysis and docs).
- **Key Deadline**: Align with class submission.

## Resources
- **Hardware**: Adafruit CPX, SG92R servo (from kit), 6-inch PVC end cap, 1/2-inch PVC pipes, 3/4-inch tee, aquarium tubing, zip ties, silicone, alligator clips (from kit), electrical tape.
- **Software**: CircuitPython (adafruit.com), Mu editor.
- **3D Printing**: Tinkercad for design; PLA filament at school makerspace.
- **References**:
  - CPX Guide: learn.adafruit.com/adafruit-circuit-playground-express.
  - Servo Tutorial: learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-servo.
  - Pinch Valve STL: thingiverse.com/thing:4530241.
  - Capacitive Sensing: learn.adafruit.com/circuitpython-essentials/circuitpython-capacitive-touch.
- **Environment**: Workbench, computer, 3D printer access.

## Risks and Mitigation
- **Risk**: Capacitive clips misfire (e.g., humidity, shorting).
  - **Mitigation**: Insulate jaws with tape/heat-shrink, calibrate thresholds, space clips apart.
- **Risk**: SG92R lacks torque to pinch tube.
  - **Mitigation**: Use soft 1/4-inch tubing, test 3D-printed arm strength.
- **Risk**: Water leaks from end cap.
  - **Mitigation**: Seal thoroughly with silicone, test with small volumes.
- **Risk**: Clip movement causes false readings.
  - **Mitigation**: Secure with tape or 3D-printed holder.

## Success Criteria
- Prototype fills container and stops via servo-driven pinch valve on level detection.
- Voting system handles single-sensor faults without false closure.
- Report addresses all challenges with code, demo, and performance analysis.
- Safe, DIY build with accessible materials.