# Challenge 4: Tension Wire Smart Actuator

This development plan outlines the design, construction, and testing of a smart actuator for Challenge 4, utilizing the Adafruit Circuit Playground Express (CPX) kit as the core microcontroller. The actuator will traverse a school-supplied tensioned steel cable, embodying Industry 4.0 principles of scalability, transportability, and interconnectivity. The plan leverages the CPX's built-in sensors (accelerometer, light/proximity), NeoPixels, and CircuitPython for rapid prototyping, with additional components for motor control and power. The timeline spans 4-6 weeks, focusing on mechatronic integration and iterative testing.

## Phase 1: Research and Planning (Week 1)
- **Define Objectives**: Build a smart actuator to move autonomously along a tensioned steel cable (1-2 meters) from one end to the other, demonstrating:
  - Scalability: Design replicable for multiple actuators.
  - Transportability: Lightweight, modular for easy relocation.
  - Interconnectivity: Interfaces with external systems via wired or wireless protocols.
- **Research Key Concepts**:
  - CPX Capabilities: Utilize onboard accelerometer for balance, light sensor for end-point detection, and I2C/SPI for add-ons.
  - Power Management: Leverage CPX’s low power draw (~20mA idle) with a LiPo battery and sleep modes.
  - UI: Use CPX’s USB for serial monitoring or a basic Python-based dashboard via Mu Editor.
  - Cable Traversal: Explore wheeled grippers or rollers for movement, considering cable tension and friction.
  - PAC Systems: Model programmable automation controller logic with CPX’s CircuitPython.
- **Brainstorm Design**: Sketch a compact actuator with CPX mounted centrally in a 3D-printed chassis, integrating a motor and rollers.
- **Milestone**: Requirements document with CPX pinout mapping (e.g., A1-A7 for sensors/motor).

## Phase 2: Design and Prototyping (Weeks 1-2)
- **Mechanical Design**:
  - Cable Setup: Use school-supplied steel cable (2-4mm diameter) tensioned with turnbuckles.
  - Actuator Body: Design a 3D-printed chassis (school printer/filament) to house CPX, motor, and cable-gripping wheels (e.g., 3D-printed with rubber O-rings).
  - Sensors: Rely on CPX’s accelerometer and light sensor; add limit switches for end-of-line detection if needed.
- **Electrical and Power Design**:
  - Power Management: Connect a LiPo battery (3.7V 500mAh, JST connector) to CPX’s JST port. Code sleep modes for efficiency (target: 15+ traversals per charge).
  - Microcontroller: Use CPX with CircuitPython for PAC-like logic and control.
- **Software and Integration**:
  - Integration Parameters: Enable wired interconnectivity via CPX’s USB; consider a Bluetooth module (e.g., HC-05) for wireless scalability.
  - UI Development: Start with serial output in Mu Editor for position and battery monitoring (via analog pin voltage divider). Optionally, develop a web UI via Bluetooth.
- **Prototype Assembly**: 3D-print initial chassis, wire CPX to a micro DC motor (e.g., N20 geared), and test on a short cable segment.
- **Milestone**: CAD files for printing; initial CPX code for motor control.

## Phase 3: Building and Implementation (Weeks 2-3)
- **Construct the Actuator**:
  - Mechanical Assembly: Print and fit chassis around CPX. Attach motor-driven wheels to grip cable; use accelerometer for tilt detection.
  - Electrical Wiring: Connect CPX to motor (via transistor or driver for current handling), battery, and optional sensors. Test on school-supplied cable.
  - Power Optimization: Implement PWM motor control and sparse sensor polling in CircuitPython.
- **Integrate Systems**:
  - Interconnectivity: Simulate Industry 4.0 by sending data (e.g., JSON over serial) to a laptop or another CPX.
  - UI Integration: Use NeoPixels for status (e.g., green for moving, red for low battery) and serial logs for monitoring.
- **Iterate Based on Feedback**: Bench-test for cable grip and vibration; refine 3D print tolerances.
- **Milestone**: Operational prototype traversing a 0.5m cable section.

## Phase 4: Testing and Evaluation (Weeks 3-4)
- **Functional Testing**:
  - Movement: Verify end-to-end traversal on full cable length. Measure speed, accuracy, and repeatability.
  - Power Management: Log consumption via CPX (target: 15+ traversals). Test under varying loads.
  - Integration: Validate data exchange with external systems (e.g., low-latency command response).
  - UI: Ensure serial/NeoPixel interface is intuitive; gather usability feedback.
- **Performance Evaluation**:
  - Industry 4.0 Metrics:
    - Scalability: Assess adaptability for longer cables or multiple actuators.
    - Transportability: Evaluate weight (<500g target) and ease of disassembly.
    - Interconnectivity: Measure data latency and reliability.
  - Quantitative: Log traversal time, energy use, and errors via CPX’s CSV library.
  - Qualitative: Document strengths (e.g., CPX modularity) and weaknesses (e.g., motor torque limits).
- **Edge Case Testing**: Program CPX for auto-stop on accelerometer-detected falls or low battery.
- **Milestone**: Test report with CPX-logged graphs (e.g., speed vs. power).

## Phase 5: Documentation and Reflection (Weeks 4-5, if extended)
- **Compile Results**: Include CPX code, wiring diagrams, 3D print files, and test data.
- **Reflect on Learnings**: Highlight CPX’s role in simplifying PAC-like control and Industry 4.0 integration.
- **Presentation Prep**: Create demo video of traversal and slides emphasizing mechatronic principles.
- **Milestone**: Deliverables package with working prototype.

## Required Materials and Tools
- **From Adafruit CPX Kit**: CPX board, USB cable, wires/jumpers, onboard sensors/NeoPixels.
- **New Components**:
  - Micro DC motor (e.g., N20 geared for torque).
  - LiPo battery (3.7V 500mAh, JST connector).
  - Wheels/rollers (3D-printed or with rubber O-rings).
  - Optional: HC-05 Bluetooth module, limit switches.
- **School-Supplied**: Tensioned steel cable, 3D printer, filament.
- **Tools**: Soldering iron (if available), multimeter, Mu Editor (free for CircuitPython).

## Potential Challenges and Mitigations
- **CPX Current Limits**: Use a motor driver (e.g., DRV8833) if motor current exceeds CPX capacity.
- **Cable Tension Variability**: Calibrate motor speed using accelerometer feedback.
- **3D Printing Issues**: Design chassis with tolerances for CPX; test-fit early.

This plan maximizes the CPX kit and school resources for a streamlined, Industry 4.0-aligned smart actuator.