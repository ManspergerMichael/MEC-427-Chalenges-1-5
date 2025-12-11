# System Overview

## Introduction

The Liquid Level Sensor System is a mechatronics training platform designed to demonstrate the integration of sensors, controls, and user calibration in a process environment. Its primary function is to detect the liquid level in a container of water and provide visual feedback through onboard indicators.

## Hardware Architecture

The system is built around the **Adafruit Circuit Playground Express (CPX)**, which serves as the central controller. The CPX utilizes its capacitive touch sensor at pin **A1**, connected via a wired alligator clip secured to the rim of the container, to detect changes in capacitance caused by the presence of liquid. This sensing method allows the system to identify when the liquid reaches a defined level.d level.

## Power and Feedback

Power is supplied by a **3.7V battery**, ensuring portability and safe operation in laboratory settings. The CPX's **NeoPixel LEDs** provide real-time feedback and are also used during manual calibration. Calibration enables adjustment for environmental conditions (humidity, temperature, container material) and for different liquids with varying dielectric properties, ensuring reliable detection across multiple scenarios.enarios.

## System Integration

This system highlights the integration of hardware (CPX, sensors, battery), software (calibration routines, LED control), and process control concepts. It serves as a practical demonstration of how mechatronic systems combine sensing, computation, and actuation to achieve robust functionality in real-world applications.

---
## Sequential Function Chart






Controller Overview
The Adafruit Circuit Playground Express (CPX) serves as the central controller for the Liquid Level Sensor System. It integrates sensing, computation, and user interface functions into a single compact platform, enabling reliable detection and calibration of liquid levels.
The CPX is powered by a 3.7V rechargeable battery, providing portable operation and safe voltage levels for laboratory use. Its capacitive touch sensor at pin A1 is configured as the primary input, connected via an alligator clip to the rim of the container. This sensor detects changes in capacitance caused by the presence of liquid, allowing the controller to determine when the water reaches the defined level.
The CPX also incorporates NeoPixel LEDs and onboard controls, which serve as both output indicators and calibration tools. The LEDs provide immediate visual feedback of sensor status, while the onboard buttons allow manual adjustment of sensitivity to account for environmental conditions (humidity, temperature, container material) and variations in liquid properties. This ensures accurate and adaptable operation across different scenarios.
Internally, the CPX executes a control program written in CircuitPython which manages sensor input, calibration routines, and output display. The program is modular, allowing easy modification for expanded functionality, such as multi-level detection or integration with external actuators.
By combining sensing, processing, and feedback in one device, the CPX demonstrates the principles of mechatronic control: integration of hardware, software, and user interaction to achieve robust system performance.
