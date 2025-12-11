# Smart Sensor Development Workflow  
**Assignment: Challenge 1 – Smart Sensor**

---

## 1. Application Description  
The smart sensor system is designed to **detect when liquid reaches a predefined level in a container**.  

- **Function**: The sensor continuously monitors the liquid level and identifies when the set threshold is reached.  
- **Conditions**: Upon detecting liquid at the target level, the sensor outputs a **HIGH signal** to the microcontroller for processing.  
- **Feedback**: The system provides a clear indication (e.g., LED, buzzer, or digital flag) that the container has reached the fill level.  
  - **Conditions**: The system will continue sending a **HIGH signal** as long as liquid is detected at the sensor point.  

---

## 2. Task Description  
- Develop a sensor system capable of accurately detecting liquid levels.  
- Integrate the sensor with a **microcontroller** for real-time monitoring and data acquisition.  
- Implement calibration routines to account for different liquid properties (density, conductivity).  
- Provide user-defined alarms for high/low levels.  
- Validate performance through testing in simulated tank conditions.  

---

## 3. Focus Area  

### Work Piece  
A **water tower model** was chosen as the work piece to develop the fill sensor because its construction and function are simple and effective for demonstration. The setup consists of **two containers**, with one suspended above the other. A hose at the bottom of the top container allows water to flow downward, while sensors are mounted on the rim of the bottom container to detect the liquid level.  

### Mechanism  
The sensor is mounted on the lower container and wired directly to a **microcontroller** for real-time monitoring.  
- **Potential Risks**:  
  - **Water damage to the microcontroller** due to proximity to the liquid environment.  
  - **Wear or damage to the sensor** if it comes into direct contact with water or other liquids.  
- **Mitigation Strategies**:  
  - Use waterproof housings or protective enclosures for the microcontroller.  
  - Employ non-contact sensor technologies (e.g., ultrasonic or capacitive) to reduce wear and prevent liquid exposure.  
  - Position wiring and electronics above the liquid line to minimize risk.  

---

## 4. Risk Assessment  

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| Sensor fouling due to residue buildup | High | Medium | Use self-cleaning or non-contact sensors |
| Incorrect readings from foam/turbulence | Medium | High | Apply filtering algorithms and sensor shielding |
| Electrical failure in wet environments | Low | High | Waterproof housing and redundant wiring |
| Calibration drift | Medium | Medium | Regular calibration and automated self-check routines |
| Power instability | Medium | Medium | Use regulated power sources and backup batteries |

---

## 5. Definition of Application  
The smart sensor application is defined as a **liquid level detection system** that uses capacitive sensing technology to monitor when tap water reaches a predefined fill level in a container. The system is powered by a microcontroller and designed for reliable operation in controlled indoor environments.  

- **Available Power**: The system is powered by an **Adafruit Circuit Playground Express microcontroller kit**, with support from a **3.7V battery pack** for portable operation.  
- **Output Requirements**: Capacitive touch sensors, connected via **wired alligator clips** mounted on the rim of the bottom container, provide detection signals and calibration data. Signal conditioning is implemented to reduce false positives caused by disturbances such as waves or splashes contacting the sensor head.  
- **Target Object**: The sensor is calibrated to detect **tap water** as the monitored liquid.  
- **Environmental Conditions**: The system is intended for use in an **indoor environment at room temperature**, ensuring stable sensor performance and minimizing environmental interference.  

---

## 6. Sensor Technologies  
For this project, the **Adafruit Circuit Playground Express (CPX) kit** was selected as the primary development platform. The CPX was recommended due to its versatility and integrated features that support rapid prototyping of smart sensor applications.  

- **Capacitive Touch Sensors**: Used to detect the presence of liquid at the container rim. These sensors provide reliable input signals and can be calibrated to minimize false positives caused by splashes or waves.  
- **LED Lights**: Integrated LEDs serve as immediate visual indicators, signaling when the liquid has reached the predefined fill level.  
- **Buttons for Controls**: Onboard buttons allow for manual calibration, reset, or user-defined input during testing and development.  
- **Microcontroller Integration**: The CPX’s built-in microcontroller processes sensor signals in real time, enabling accurate monitoring and feedback.  
- **Expandable Features**: The CPX supports additional modules and external connections, making it adaptable for future enhancements or alternative sensing methods.  

This combination of features makes the CPX kit an effective choice for developing and testing the liquid level smart sensor, while also simplifying the workflow by reducing the need for external components.  