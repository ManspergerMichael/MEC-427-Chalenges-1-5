# Challenge 3: Wiring Diagram
## Smart Actuator - Voting Sensor + Servo Pinch Valve

```
┌─────────────────────────────────────────────────────────────────┐
│                  Circuit Playground Express (CPX)               │
│                                                                 │
│    ┌──────┐                                         ┌──────┐   │
│    │  A1  ├─────────────────────────────────────────┤Probe1│   │
│    └──────┘                                         └──────┘   │
│                                                                 │
│    ┌──────┐                                         ┌──────┐   │
│    │  A2  ├─────────────────────────────────────────┤Probe2│   │
│    └──────┘                                         └──────┘   │
│                                                                 │
│    ┌──────┐                                         ┌──────┐   │
│    │  A3  ├─────────────────────────────────────────┤Probe3│   │
│    └──────┘                                         └──────┘   │
│                                                                 │
│    ┌──────┐                                                    │
│    │  A6  ├─────────┐                                          │
│    └──────┘         │                                          │
│                     │                                          │
│    ┌──────┐         │      ┌─────────────────────────┐        │
│    │ GND  ├─────────┼──────┤        SG92R Servo      │        │
│    └──────┘         │      │  (External Power Reqd)  │        │
│                     │      └─────────────────────────┘        │
│    ┌──────┐         │                                          │
│    │ VOUT ├─────────┼─(NOT USED - See External Power Below)   │
│    └──────┘         │                                          │
│                     │                                          │
└─────────────────────┼──────────────────────────────────────────┘
                      │
                      │
            ┌─────────▼──────────┐
            │   SG92R SERVO      │
            │   CONNECTIONS:     │
            ├────────────────────┤
            │ BROWN  = GND       │◄──── Connect to CPX GND
            │ ORANGE = +5V       │◄──── Connect to External 5V Supply
            │ YELLOW = Signal    │◄──── Connect to CPX A6
            └────────────────────┘
```

---

## Component List

### Required Hardware

1. **Circuit Playground Express (CPX)**
   - Main microcontroller

2. **SG92R Servo Motor** (or compatible 5V micro servo)
   - Operating voltage: 4.8-6V
   - Operating current: ~250mA (under load)
   - Control signal: PWM (50Hz)

3. **Capacitive Touch Probes (3x)**
   - Bare copper wire, alligator clips, or conductive tape
   - Length: 4-6 inches recommended
   - Gauge: 22-24 AWG solid core wire works well

4. **External Power Supply for Servo**
   - **5V DC, 500mA+ recommended**
   - Options:
     - USB power bank (5V output)
     - 4x AA battery holder (4.8-6V)
     - Bench power supply (5V setting)
   - ⚠️ **DO NOT power servo from CPX VOUT** - insufficient current capacity

5. **Pinch Valve Mechanism** (your implementation)
   - Flexible tubing (silicone recommended)
   - Servo horn/arm attachment
   - Mounting bracket/frame

---

## Detailed Wiring Instructions

### Step 1: Capacitive Sensor Connections

**Probe 1 → A1**
- Strip 1/4" of wire insulation
- Insert into CPX pad A1 or use alligator clip
- Sensing tip: 1-2" exposed bare wire at far end
- Insulate all wire except sensing tip

**Probe 2 → A3**
- Same as Probe 1, connect to A3

**Probe 3 → A5**
- Same as Probe 1, connect to A5

**Probe Placement:**
```
Container/Tank View:
┌─────────────────┐
│                 │
│   ●  Probe 1    │  ← Spread probes apart
│      (A1)       │    Non-adjacent pads reduce
│                 │    capacitive cross-talk
│        ●  Probe 2   
│           (A3)  │
│                 │
│   ●  Probe 3    │
│      (A5)       │
│                 │
└─────────────────┘
```

---

### Step 2: Servo Motor Connections

**Servo Wire Colors (Your Servo):**
- **BROWN** = Ground (GND)
- **ORANGE** = Power (+5V)
- **YELLOW** = PWM Signal

**Connections:**

1. **BROWN (GND) → CPX GND**
   - Use any available GND pad on CPX
   - ⚠️ **CRITICAL**: Servo GND MUST share common ground with CPX

2. **YELLOW (Signal) → CPX A6**
   - This is the PWM control signal
   - CPX sends 50Hz pulses to control servo position
   - Duty cycle: 1.0ms (0°) to 1.5ms (90°)

3. **ORANGE (Power) → External 5V Supply (+)**
   - Connect to **positive terminal** of external power source
   - **DO NOT connect to CPX VOUT** (insufficient current)

4. **External Power GND → CPX GND**
   - Connect **negative terminal** of external power to CPX GND
   - Creates common ground reference (required for PWM signal)

---

### Step 3: External Power Setup

**Option A: USB Power Bank**
```
USB Power Bank (5V, 1A+)
    │
    ├─── USB cable ───> Cut cable and expose wires
    │                   RED (+5V) ──> Servo ORANGE
    │                   BLACK (GND) ──> Servo BROWN + CPX GND
```

**Option B: Battery Pack**
```
4x AA Batteries (6V total)
    │
    ├─── (+) Terminal ──> Servo ORANGE
    └─── (-) Terminal ──> Servo BROWN + CPX GND
```

**Option C: Bench Power Supply**
```
Bench PSU (set to 5.0V, limit 500mA)
    │
    ├─── (+) Red Terminal ──> Servo ORANGE
    └─── (-) Black Terminal ──> Servo BROWN + CPX GND
```

---

## Complete Wiring Schematic

```
                    ┌─────────────────────┐
                    │   External 5V PSU   │
                    │   (500mA minimum)   │
                    └──────┬──────┬───────┘
                           │      │
                          +5V    GND
                           │      │
        ┌──────────────────┼──────┼─────────────────────┐
        │                  │      │                     │
        │  CPX             │      │                     │
        │                  │      │                     │
        │  A1 ●────────────┼──────┼─────► Probe 1      │
        │                  │      │                     │
        │  A2 ●────────────┼──────┼─────► Probe 2      │
        │                  │      │                     │
        │  A3 ●────────────┼──────┼─────► Probe 3      │
        │                  │      │                     │
        │  A6 ●────────────┼──────┼───┐                │
        │                  │      │   │                │
        │ GND ●────────────┼──────┴───┼────┐           │
        │                  │          │    │           │
        └──────────────────┼──────────┼────┼───────────┘
                           │          │    │
                           │          │    │
                     ┌─────▼──────────▼────▼─────┐
                     │      SG92R SERVO          │
                     │                           │
                     │  ORANGE = +5V (External)  │
                     │  YELLOW = Signal (A6)     │
                     │  BROWN  = GND (Common)    │
                     └───────────────────────────┘
```

---

## Safety & Best Practices

### ⚠️ **CRITICAL WARNINGS**

1. **DO NOT power servo from CPX VOUT**
   - CPX VOUT max current: ~200mA
   - Servo stall current: 250-500mA
   - **Risk**: Brownout, CPX reset, USB port damage

2. **ALWAYS connect common ground**
   - External power GND MUST connect to CPX GND
   - Without common ground, PWM signal will not work correctly

3. **Use appropriate wire gauge**
   - Servo power wires: 22 AWG or thicker
   - Signal wires: 24-26 AWG acceptable

4. **Secure all connections**
   - Loose wires can cause intermittent operation
   - Use solder or secure screw terminals for power connections

### ✅ **Best Practices**

1. **Test servo separately first**
   - Use `Servo_Test.py` to verify servo operation
   - Confirm full range of motion (0° to 90°)

2. **Calibrate probes with valve OPEN**
   - Run calibration with no water present
   - Ensures accurate baseline readings

3. **Mount CPX on non-conductive surface**
   - Plastic mounting reduces ground coupling noise
   - Keeps sensor readings stable

4. **Keep servo wires short**
   - Minimize signal wire length to A6
   - Reduces electrical noise and voltage drop

5. **Add optional capacitor**
   - 100-470µF across servo power (+/-)
   - Smooths power spikes during servo motion
   - Not required but recommended for stability

---

## Pinch Valve Mechanical Setup

### Suggested Mounting

```
Side View:
                  Servo Motor
                  ┌────────┐
                  │ SG92R  │
                  └────┬───┘
                       │ Servo Horn (arm)
                       ▼
                  ┌────────┐
                  │ Pinch  │  ← Presses down on tube
                  │ Plate  │
                  └────┬───┘
                       │
    ═══════════════════●═══════════════════  ← Flexible tubing
                     Pinch point
                       ▲
                  ┌────┴───┐
                  │ Base   │
                  │ Plate  │
                  └────────┘
```

**Components:**
- **Servo Horn**: Attached to servo shaft
- **Pinch Plate**: Flat surface (plastic, metal) to compress tube
- **Flexible Tubing**: Silicone (4-6mm OD recommended)
- **Base Plate**: Provides back-pressure for pinching

**Servo Positions:**
- **0° (SERVO_OPEN)**: Horn up, tube unrestricted
- **90° (SERVO_CLOSED)**: Horn down, tube fully pinched

---

## Testing Procedure

### 1. Hardware Check (No Code)
- [ ] All 3 probes connected to A1, A2, A3
- [ ] Servo YELLOW connected to A6
- [ ] Servo BROWN connected to CPX GND
- [ ] Servo ORANGE connected to external 5V supply
- [ ] External power GND connected to CPX GND
- [ ] CPX powered via USB

### 2. Servo Test
```bash
# Deploy Servo_Test.py to CPX
# Observe servo moving through positions
# Verify full range of motion
```

### 3. Sensor Test (Dry)
```bash
# Deploy code.py to CPX
# Check serial output:
# - Baselines should be ~1500-1700 per probe
# - All probes show "wet: False"
# - Majority: False
# - Red LED: OFF
```

### 4. Sensor Test (Wet)
```bash
# Touch 2 probes with wet finger or water
# Check serial output:
# - 2 probes show "wet: True"
# - Majority: True
# - Red LED: ON
# - Servo closes valve
```

### 5. Full System Test
```bash
# With valve mechanism installed:
# 1. Power on (valve should open)
# 2. Touch 2+ probes to water
# 3. Valve should close (verify tube pinched)
# 4. Remove probes from water
# 5. Valve should open (verify tube unpinched)
```

---

## Troubleshooting

### Servo doesn't move
- ✓ Check external power supply is ON and 5V
- ✓ Verify YELLOW wire connected to A6
- ✓ Verify ORANGE wire connected to external +5V
- ✓ Verify BROWN wire connected to CPX GND
- ✓ Confirm common ground (GND) between CPX and external power
- ✓ Test with `Servo_Test.py`

### Servo jitters/buzzes
- ✓ Add 100µF capacitor across servo power
- ✓ Check power supply current capacity (500mA+)
- ✓ Reduce servo load (pinch valve may be too tight)

### Sensors don't detect water
- ✓ Verify probes connected to A1, A2, A3
- ✓ Check baselines in serial output
- ✓ Adjust threshold margin with Button B
- ✓ Hold Button A for 2s to recalibrate

### Red LED on but no water detected
- ✓ Threshold margin too low (increase with Button B)
- ✓ Recalibrate baselines (hold Button A)
- ✓ Check for electrical noise (move CPX to plastic surface)

### Valve doesn't fully close/open
- ✓ Adjust `SERVO_OPEN` and `SERVO_CLOSED` values in code
- ✓ Check servo horn alignment
- ✓ Verify tube flexibility (silicone works best)

---

## Code Constants Reference

```python
# Servo PWM duty cycles (adjust if needed)
SERVO_OPEN = 3277      # 1.0ms pulse = 0° (valve open)
SERVO_CLOSED = 4915    # 1.5ms pulse = 90° (valve closed)

# Sensor thresholds
threshold_margin = 1000  # Default sensitivity (adjustable with A/B buttons)

# Detection voting
# Requires 2 out of 3 probes to detect water
majority_wet = (probe_wet.count(True) >= 2)
```

---

## Visual Feedback (NeoPixels)

**LED Pattern:**
- **Pixels 0-2**: Probe 1 (A1) status
  - Cyan = wet detected
  - Dim green = dry
- **Pixels 3-5**: Probe 2 (A3) status
- **Pixels 6-8**: Probe 3 (A5) status
- **Pixel 9**: Majority vote result
  - Red = majority wet (valve closed)
  - Green = majority dry (valve open)

**Red Status LED:**
- ON = Water detected (majority), valve closed
- OFF = No water (majority), valve open

---

*Wiring diagram created for MEC 427 Challenge 3*  
*Date: November 30, 2025*
