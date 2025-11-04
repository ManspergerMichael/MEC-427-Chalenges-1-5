# MEC 427 — Smart Sensor and Actuator System (Challenges 1–3)

This repository contains the work for MEC 427 Smart Systems Challenges 1–3 using an Adafruit Circuit Playground Express (CPX) with CircuitPython. For the full design and schedule, see `Ch1,2,3/CombinedSmartSystemPlan.markdown`.

## Objective

Build and demonstrate a fluid control system using a 6-inch PVC end-cap tank suspended on a PVC tripod. Detect water level in a lower container using three CPX capacitive touch sensors (alligator clips) with a majority-vote scheme, and drive a 3D‑printed tube‑pinch valve using a TowerPro SG92R servo to prevent overflow.

## Challenge 1 — Fluid Level Sensor (Capacitive)

- Use CPX capacitive touch (`touchio.TouchIn`) on A1 to sense water presence via an alligator-clip probe.
- Calibrate a threshold (start ≈ 1000, adjust during testing) and provide feedback with NeoPixels + serial prints.
- Goal: Reliably detect when water reaches the probe depth.

## Challenge 2 — Voting Sensor System (Redundancy)

- Expand to three probes on pads A1–A3, positioned at similar heights.
- Implement majority voting: “level reached” when ≥2 sensors exceed the threshold.
- Goal: Robust detection that tolerates a single sensor fault or noise.

## Challenge 3 — Smart Actuator System (Pinch Valve)

- 3D‑print a pinch‑valve mechanism and mount an SG92R servo to pinch 1/4" tubing.
- Wire servo: signal → A6, power → VOUT, ground → GND.
- Logic: On “level reached,” set `servo.angle = 90` to close the valve; provide a button (e.g., `button_a`) action to reset/open.

---

For detailed build notes, materials, timeline, and risks, see `Ch1,2,3/CombinedSmartSystemPlan.markdown`. The CPX runtime code lives in `Challenge_1/code.py`.
