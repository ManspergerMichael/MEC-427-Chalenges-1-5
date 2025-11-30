# Challenge 3 Unit Testing

## Overview
Unit tests for the Smart Actuator voting logic, hysteresis, threshold calculations, and auto-tracking features.

## Running Tests

### Run all tests:
```bash
python test_code.py
```

### Run with verbose output:
```bash
python test_code.py -v
```

### Run specific test class:
```bash
python -m unittest test_code.TestVotingLogic
```

### Run specific test method:
```bash
python -m unittest test_code.TestVotingLogic.test_majority_vote_two_true
```

## Test Coverage

### TestVotingLogic
Tests the majority voting mechanism (2 out of 3 probes):
- ✓ Two probes wet triggers majority
- ✓ Three probes wet triggers majority
- ✓ One probe wet does not trigger majority
- ✓ Zero probes wet does not trigger majority

### TestHysteresisLogic
Tests the hysteresis counter system:
- ✓ Wet count increments when out of threshold
- ✓ Dry count increments when within threshold
- ✓ Counts don't exceed maximum (3)
- ✓ Probe state changes at count >= 2

### TestThresholdCalculation
Tests threshold and margin calculations:
- ✓ High/low thresholds calculated from baselines
- ✓ Margin decrease with button A
- ✓ Margin increase with button B
- ✓ Margin limits (0 minimum, 8000 maximum)

### TestAutoTracking
Tests baseline drift compensation:
- ✓ Baseline adjusts upward for higher readings
- ✓ Baseline adjusts downward for lower readings
- ✓ No adjustment for small differences
- ✓ Tracking only when all probes dry
- ✓ Tracking disabled when wet

### TestBaselineCapture
Tests calibration logic:
- ✓ Median value selection from readings
- ✓ Readings properly sorted

### TestServoControl
Tests servo state management:
- ✓ PWM values are correct and distinct
- ✓ State change detection (dry→wet, wet→dry, no change)

## Expected Output

```
..................................
----------------------------------------------------------------------
Ran 34 tests in 0.001s

OK
```

## Adding New Tests

1. Create a new test class inheriting from `unittest.TestCase`
2. Add test methods starting with `test_`
3. Use assertions: `assertEqual`, `assertTrue`, `assertFalse`, etc.
4. Run tests to verify

Example:
```python
class TestNewFeature(unittest.TestCase):
    def test_feature_behavior(self):
        result = my_function(input_value)
        self.assertEqual(result, expected_value)
```

## Integration Testing

Note: These unit tests cover logic only. For hardware integration testing:
1. Deploy code to CIRCUITPY
2. Manually test with actual probes and servo
3. Verify LED feedback matches probe states
4. Test button sensitivity adjustments
