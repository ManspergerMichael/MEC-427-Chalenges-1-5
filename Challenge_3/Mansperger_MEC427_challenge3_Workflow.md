# Smart Actuator Development Workflow  
**Assignment: Challenge 3 – Smart Actuator**

---

## 1. Application Description  
The smart actuator system is designed to **control water flow between two containers** using a servo-driven pinch valve.  

- **Function**: A Tower Pro SG92R micro servo, wired to the Adafruit CPX, actuates a 3D-printed pinch valve.  
- **Conditions**: The valve is mounted on a leg of the tower between the upper and lower containers. The hose passes through the valve, allowing the servo to open or close water flow.  
- **Feedback**: The actuator responds to sensor signals from the lower container, enabling automated control of water transfer.  

---

## 2. Task Description  
- Integrate a **Tower Pro SG92R micro servo** with the Adafruit CPX microcontroller.  
- Mount the servo into a **3D-printed pinch valve** for mechanical actuation.  
- Position the valve between the upper and lower containers, with the hose routed through it.  
- Link actuator control to sensor feedback from the lower container.  
- Validate performance by testing water flow regulation under different sensor conditions.  

---

## 3. Focus Area  

### Work Piece  
The **water tower model** remains the chosen work piece. The pinch valve is mounted on a tower leg between the upper and lower containers, with the hose routed through the valve to the lower container where sensors are mounted.  

### Mechanism  
The servo rotates to compress or release the hose inside the pinch valve, controlling water flow.  
- **Potential Risks**:  
  - **Servo wear** from repeated actuation.  
  - **Valve misalignment** causing incomplete closure or leakage.  
  - **Water exposure** to servo or electronics.  
- **Mitigation Strategies**:  
  - Use durable servo mounts and limit actuation cycles.  
  - Ensure precise 3D printing and alignment of the valve.  
  - Apply waterproofing or protective housing for electronics.  

---

## 4. Risk Assessment  

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| Servo wear from repeated cycles | Medium | Medium | Limit duty cycles, use robust mounting |
| Valve misalignment or leakage | Medium | High | Precision 3D printing and calibration |
| Water exposure to servo/electronics | Low | High | Waterproof housing and protective placement |
| Power instability | Medium | Medium | Use regulated power sources and backup batteries |

---

## 5. Definition of Application  
The smart actuator application is defined as a **servo-controlled pinch valve system** that regulates water flow between two containers based on sensor feedback.  

- **Available Power**: Powered by the **Adafruit Circuit Playground Express kit** with a **3.7V battery pack**.  
- **Output Requirements**: The Tower Pro SG92R servo actuates the pinch valve to open or close water flow. Control signals are processed by the CPX based on sensor input.  
- **Target Object**: Tap water flowing through the hose between containers.  
- **Environmental Conditions**: Designed for **indoor use at room temperature**, ensuring stable actuator performance.  

---

## 6. Actuator Technologies  
For this project, the **Tower Pro SG92R micro servo** was selected as the actuator due to its compatibility with the CPX and suitability for small-scale mechanical control.  

- **Micro Servo (SG92R)**: Provides rotational motion to actuate the pinch valve.  
- **3D-Printed Pinch Valve**: Converts servo rotation into hose compression, regulating water flow.  
- **Microcontroller Integration (CPX)**: Processes sensor signals and drives the servo accordingly.  
- **LED/Feedback Indicators**: CPX LEDs can signal valve state (open/closed).  
- **Expandable Features**: The system can be extended to include multiple valves or automated flow control routines.  

This combination of servo actuation and CPX integration makes the system an effective demonstration of smart actuator control in a liquid transfer application.  