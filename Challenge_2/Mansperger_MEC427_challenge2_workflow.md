# Technical Data Package  
**Assignment: Challenge 2 – Smart Sensor**

---

## 1. Application Description  
The smart sensor system is designed to **detect when liquid reaches a predefined level in a container** using a **voting sensor array**.  

- **Function**: Three capacitive touch sensors are mounted at the same water level. Each sensor independently detects liquid presence.  
- **Conditions**: When liquid reaches the sensor line, each sensor outputs a **HIGH signal** to the microcontroller.  
- **Feedback**: The microcontroller applies a **majority voting algorithm**. If at least two sensors detect liquid, the system confirms the fill level and signals accordingly.  
  - **Conditions**: The system continues to send a HIGH signal as long as the majority of sensors detect liquid.  

---

## 2. Task Description  
- Develop a sensor system with **three capacitive touch sensors** connected to the Adafruit CPX microcontroller.  
- Implement a **voting algorithm** to determine liquid detection based on majority agreement.  
- Provide feedback through LEDs or buzzers when the fill level is confirmed.  
- Validate performance by testing with tap water in a controlled water tower model.  
- Compare reliability against single-sensor detection.  

---

## 3. Focus Area  

### Work Piece  
The **water tower model** remains the chosen work piece. Three capacitive sensors are mounted at the same height on the rim of the bottom container to detect liquid presence at the fill level.  

### Mechanism  
The sensors are wired to the CPX microcontroller, which processes their signals and applies a voting algorithm.  
- **Potential Risks**:  
  - **Water damage to the microcontroller** due to proximity to liquid.  
  - **Sensor wear or damage** if sensors touch the liquid directly.  
  - **Disagreement between sensors** due to noise or calibration drift.  
- **Mitigation Strategies**:  
  - Waterproof housing for the CPX.  
  - Protective coatings or non-contact sensor placement.  
  - Regular calibration and signal conditioning to reduce false positives.  
  - Voting logic ensures reliability even if one sensor fails.  

---

## 4. Risk Assessment  

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| Incorrect readings from foam/turbulence | Medium | High | Apply filtering algorithms and sensor shielding |
| Calibration drift across sensors | Medium | Medium | Regular calibration and automated self-check routines |
| Sensor disagreement (false positives/negatives) | Medium | Medium | Majority voting algorithm ensures reliable detection |
| Power instability | Medium | Medium | Use regulated power sources and backup batteries |

---

## 5. Definition of Application  
The smart sensor application is defined as a **redundant liquid level detection system** that uses a voting sensor array to improve reliability. By requiring majority agreement among three capacitive sensors, the system reduces false positives and ensures robust detection.  

- **Available Power**: Powered by the **Adafruit Circuit Playground Express kit**, with a **3.7V battery pack** for portable operation.  
- **Output Requirements**: Three capacitive touch sensors connected via alligator clips provide detection signals. The CPX applies voting logic and outputs confirmation signals through LEDs or buzzers.  
- **Target Object**: The system is calibrated to detect **tap water**.  
- **Environmental Conditions**: Designed for **indoor use at room temperature**, ensuring stable sensor performance.  

---

## 6. Sensor Technologies  
The **Adafruit Circuit Playground Express (CPX) kit** was selected as the development platform due to its versatility and integrated features.  

- **Capacitive Touch Sensors**: Three sensors detect liquid presence at the same level, providing redundant input for voting logic.  
- **LED Lights**: Integrated LEDs indicate when the majority of sensors confirm the fill level.  
- **Buttons for Controls**: Onboard buttons allow calibration, reset, or manual input during testing.  
- **Microcontroller Integration**: The CPX processes signals from all three sensors in real time, applying majority voting to ensure reliable detection.  
- **Expandable Features**: The CPX supports additional modules and external connections, making it adaptable for future enhancements.  

This combination of features makes the CPX kit an effective choice for developing and testing a **voting sensor array** for liquid level detection.  