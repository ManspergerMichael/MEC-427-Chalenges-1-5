# Challenge 2: Voting Capacitive Water Sensor - Calibration Guide

## System Overview

This capacitive water sensor uses a **3-sensor voting array** with majority logic detection. The system requires at least 2 out of 3 sensors to detect water before triggering, providing fault tolerance and preventing false positives.

### Hardware Configuration
- **Sensors**: 3 non-adjacent capacitive touch pads (A1, A3, A5)
- **Sensor Spacing**: Non-adjacent pins to reduce cross-talk and electrical coupling
- **Mounting**: CPX on plastic mount to eliminate ground coupling issues
- **Probes**: Direct wire connection (no alligator clips) for stable readings

### Detection Logic
- **Majority Voting**: Requires 2 out of 3 sensors to agree
- **Bidirectional Detection**: Triggers on large delta changes (positive OR negative)
- **Smoothing**: EMA filter (α=0.3) for noise reduction
- **Hysteresis**: 2-sample confirmation to prevent flickering

---

## Calibration Procedure

### Step 1: Physical Setup
1. **Mount the CPX** on a non-conductive (plastic) surface
2. **Attach probes** to pads A1, A3, and A5:
   - Use direct wire connections (avoid alligator clips if possible)
   - Insulate all wiring except the sensing tips
   - Space probes physically in the container to reduce coupling
3. **Ensure all probes are DRY** before powering on

### Step 2: Auto-Calibration on Boot
1. **Remove all probes from water** (critical!)
2. **Connect CPX to power** or press the reset button
3. **Observe pixel 0 turn amber** - calibration in progress
4. **Wait 6 seconds** for calibration to complete (120 samples per sensor)
5. **Pixel 0 turns off** - calibration complete, dry baselines captured

**Important**: If probes are wet during calibration, the system will not work correctly. Always recalibrate with dry probes.

### Step 3: Verify Dry Baseline
Open serial monitor and check the output with all probes dry:
```
r: [1709, 1682, 1551] d: [-6, -1, -16] ... wet: [False, False, False] maj: False
```

- `r:` Raw sensor values (should be stable)
- `d:` Delta from baseline (should be near 0, typically ±20 counts)
- `wet:` Per-sensor flags (should all be False)
- `maj:` Majority decision (should be False)

### Step 4: Test Single Probe Detection
1. **Immerse only one probe** in water
2. **Check serial output**:
   ```
   wet: [True, False, False] maj: False
   ```
   - One sensor shows `True`
   - Majority (`maj`) remains `False` (1 out of 3 is not enough)

### Step 5: Test Majority Voting
1. **Immerse two probes** in water
2. **Check serial output**:
   ```
   wet: [True, True, False] maj: True
   ```
   - Two sensors show `True`
   - Majority (`maj`) is now `True` (2 out of 3)
   - **Red LED turns on**

### Step 6: Test All-Probes Detection
1. **Immerse all three probes** in water
2. **Check serial output**:
   ```
   r: [16, 22, 16] d: [-1705, -1665, -1543] ... wet: [True, True, True] maj: True
   ```
   - All sensors show `True`
   - Deltas are **negative** (common-mode shift in conductive water)
   - Detection still works (bidirectional logic handles this)
   - **Amber bar graph shows magnitude** of change

### Step 7: Manual Threshold Adjustment (Optional)
If detection is too sensitive or not sensitive enough:

- **Button A**: Decrease margin (more sensitive, lower threshold)
- **Button B**: Increase margin (less sensitive, higher threshold)
- **Hold A+B for 1 second**: Save current margin to `cal.txt` (green flash confirms)

Current default margin: **1000 counts**

---

## Understanding Serial Debug Output

Example output:
```
r: [1709, 1682, 1551] d: [-6, -1, -16] thr_lo: [722, 673, 577] thr_hi: [2722, 2673, 2577] wet: [False, False, False] maj: False margin: 1000
```

### Field Definitions
- **r:** Raw capacitance readings per sensor [A1, A3, A5]
- **d:** Delta from baseline (raw - baseline) per sensor
- **thr_lo:** Lower threshold (baseline - margin) per sensor
- **thr_hi:** Upper threshold (baseline + margin) per sensor
- **wet:** Per-sensor detection flags (True if |delta| > margin)
- **maj:** Majority voting result (True if ≥2 sensors detect water)
- **margin:** Current threshold margin (adjustable with A/B buttons)

---

## Expected Behavior Summary

### Dry Condition
- Deltas: ±20 counts or less
- Wet flags: All False
- Majority: False
- Red LED: Off
- Bar graph: Minimal or no amber bar

### One Probe Wet
- Deltas: One large (±1000-2000), others small
- Wet flags: One True, two False
- Majority: **False** (fault tolerance - single sensor ignored)
- Red LED: Off

### Two Probes Wet
- Deltas: Two large, one small
- Wet flags: Two True, one False
- Majority: **True** (2/3 consensus reached)
- Red LED: On
- Bar graph: Large amber bar

### Three Probes Wet
- Deltas: All large (may be negative due to common-mode shift)
- Wet flags: All True
- Majority: **True**
- Red LED: On
- Bar graph: Large amber bar

---

## Troubleshooting

### Problem: Erratic delta readings
**Causes:**
- Alligator clips with poor contact
- CPX on metal/conductive surface
- Probes too close together

**Solutions:**
- Use direct wire connections (solder + heat shrink)
- Mount CPX on plastic
- Space probes farther apart in container

### Problem: Negative deltas when all probes are wet
**Status:** Normal behavior
- Conductive water creates common-mode voltage shift
- Bidirectional detection handles this automatically
- System triggers correctly on absolute delta magnitude

### Problem: False triggers when dry
**Cause:** Threshold margin too low

**Solution:**
- Press Button B to increase margin
- Hold A+B to save new setting

### Problem: No detection when wet
**Causes:**
- Calibrated while probes were wet
- Threshold margin too high
- Poor probe contact with water

**Solutions:**
1. Reset CPX with dry probes to recalibrate
2. Press Button A to decrease margin
3. Check probe insulation - ensure sensing tips are exposed

### Problem: Bar graph disappears when wet
**Status:** Fixed in current version
- Display now uses absolute delta magnitude
- Works correctly with both positive and negative deltas

---

## Technical Details

### Noise Filtering
- **EMA Smoothing**: α = 0.3 (70% previous + 30% new reading)
- **Calibration**: 120-sample median per sensor (6 seconds)
- **Hysteresis**: 2-sample confirmation (wet_count ≥ 2)

### Signal Characteristics
- **Dry baseline**: ~1500-1700 counts (varies per sensor)
- **Single wet delta**: +1000 to +2000 counts (positive)
- **Multi wet delta**: -1500 to -1700 counts (negative, common-mode shift)
- **Default margin**: 1000 counts

### Physical Considerations
- **Electrode area**: Larger = more sensitivity
- **Wire length**: Shorter = less noise
- **Probe spacing**: Farther = less coupling
- **Water conductivity**: Higher = stronger common-mode effect

---

## Recommended Workflow

1. **Setup**: Mount CPX on plastic, attach dry probes
2. **Calibrate**: Power on with dry probes, wait 6 seconds
3. **Verify**: Check serial - deltas near 0 when dry
4. **Test voting**: 1 probe (maj: False), 2 probes (maj: True), 3 probes (maj: True)
5. **Tune** (if needed): Adjust margin with A/B buttons
6. **Save**: Hold A+B to save threshold to persistent storage

---

## Version History

**Current Version**: V3 Final
- Multi-sensor voting array (A1, A3, A5)
- Majority logic (2 out of 3)
- Bidirectional delta detection
- Absolute magnitude bar graph display
- EMA smoothing (α=0.3)
- Enhanced calibration (120 samples)
- Serial debug output

---

## Files
- **code.py**: Main sensor code (deployed to CPX)
- **cal.txt**: Saved threshold margin (created when A+B held)
- **CALIBRATION_GUIDE.md**: This document

---

*Last Updated: November 11, 2025*
