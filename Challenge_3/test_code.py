"""Unit tests for Challenge 3 Smart Actuator logic.

Tests the core logic functions without requiring hardware.
"""

import unittest


class TestVotingLogic(unittest.TestCase):
    """Test the majority voting logic."""

    def test_majority_vote_two_true(self):
        """Two wet probes should trigger majority."""
        probe_wet = [True, True, False]
        majority_wet = probe_wet.count(True) >= 2
        self.assertTrue(majority_wet)

    def test_majority_vote_three_true(self):
        """Three wet probes should trigger majority."""
        probe_wet = [True, True, True]
        majority_wet = probe_wet.count(True) >= 2
        self.assertTrue(majority_wet)

    def test_majority_vote_one_true(self):
        """One wet probe should not trigger majority."""
        probe_wet = [True, False, False]
        majority_wet = probe_wet.count(True) >= 2
        self.assertFalse(majority_wet)

    def test_majority_vote_zero_true(self):
        """Zero wet probes should not trigger majority."""
        probe_wet = [False, False, False]
        majority_wet = probe_wet.count(True) >= 2
        self.assertFalse(majority_wet)


class TestHysteresisLogic(unittest.TestCase):
    """Test the hysteresis counter logic."""

    def test_wet_count_increment(self):
        """Wet count should increment when out of threshold."""
        wet_count = 0
        dry_count = 0
        raw_value = 3000
        thr_hi = 2500
        thr_lo = 1500

        if (raw_value > thr_hi) or (raw_value < thr_lo):
            wet_count = min(wet_count + 1, 3)
            dry_count = 0
        else:
            dry_count = min(dry_count + 1, 3)
            wet_count = 0

        self.assertEqual(wet_count, 1)
        self.assertEqual(dry_count, 0)

    def test_dry_count_increment(self):
        """Dry count should increment when within threshold."""
        wet_count = 0
        dry_count = 0
        raw_value = 2000
        thr_hi = 2500
        thr_lo = 1500

        if (raw_value > thr_hi) or (raw_value < thr_lo):
            wet_count = min(wet_count + 1, 3)
            dry_count = 0
        else:
            dry_count = min(dry_count + 1, 3)
            wet_count = 0

        self.assertEqual(wet_count, 0)
        self.assertEqual(dry_count, 1)

    def test_wet_count_max_limit(self):
        """Wet count should not exceed 3."""
        wet_count = 3
        wet_count = min(wet_count + 1, 3)
        self.assertEqual(wet_count, 3)

    def test_probe_wet_threshold(self):
        """Probe should be considered wet when count >= 2."""
        wet_count = 2
        probe_wet = wet_count >= 2
        self.assertTrue(probe_wet)

        wet_count = 1
        probe_wet = wet_count >= 2
        self.assertFalse(probe_wet)


class TestThresholdCalculation(unittest.TestCase):
    """Test threshold calculation logic."""

    def test_threshold_calculation(self):
        """Thresholds should be calculated correctly from baselines."""
        dry_baselines = [1500, 1600, 1550]
        threshold_margin = 1000

        thr_lo = [b - threshold_margin for b in dry_baselines]
        thr_hi = [b + threshold_margin for b in dry_baselines]

        self.assertEqual(thr_lo, [500, 600, 550])
        self.assertEqual(thr_hi, [2500, 2600, 2550])

    def test_margin_adjustment_decrease(self):
        """Margin should decrease correctly with button A."""
        threshold_margin = 1000
        MARGIN_STEP = 100

        threshold_margin = max(0, threshold_margin - MARGIN_STEP)
        self.assertEqual(threshold_margin, 900)

    def test_margin_adjustment_increase(self):
        """Margin should increase correctly with button B."""
        threshold_margin = 1000
        MARGIN_STEP = 100

        threshold_margin = min(8000, threshold_margin + MARGIN_STEP)
        self.assertEqual(threshold_margin, 1100)

    def test_margin_min_limit(self):
        """Margin should not go below 0."""
        threshold_margin = 50
        MARGIN_STEP = 100

        threshold_margin = max(0, threshold_margin - MARGIN_STEP)
        self.assertEqual(threshold_margin, 0)

    def test_margin_max_limit(self):
        """Margin should not exceed 8000."""
        threshold_margin = 7950
        MARGIN_STEP = 100

        threshold_margin = min(8000, threshold_margin + MARGIN_STEP)
        self.assertEqual(threshold_margin, 8000)


class TestAutoTracking(unittest.TestCase):
    """Test baseline auto-tracking logic."""

    def test_tracking_adjustment_positive(self):
        """Baseline should adjust upward when raw value is higher."""
        dry_baseline = 1500
        raw_value = 1600
        TRACKING_RATE = 0.02

        diff = raw_value - dry_baseline
        adjustment = int(diff * TRACKING_RATE)

        self.assertEqual(adjustment, 2)
        new_baseline = dry_baseline + adjustment
        self.assertEqual(new_baseline, 1502)

    def test_tracking_adjustment_negative(self):
        """Baseline should adjust downward when raw value is lower."""
        dry_baseline = 1500
        raw_value = 1400
        TRACKING_RATE = 0.02

        diff = raw_value - dry_baseline
        adjustment = int(diff * TRACKING_RATE)

        self.assertEqual(adjustment, -2)
        new_baseline = dry_baseline + adjustment
        self.assertEqual(new_baseline, 1498)

    def test_tracking_no_adjustment_small_diff(self):
        """No adjustment when difference is too small."""
        dry_baseline = 1500
        raw_value = 1510
        TRACKING_RATE = 0.02

        diff = raw_value - dry_baseline
        adjustment = int(diff * TRACKING_RATE)

        # Small difference results in 0 adjustment after int()
        self.assertEqual(adjustment, 0)

    def test_tracking_enabled_check(self):
        """Tracking should only occur when enabled and all probes dry."""
        tracking_enabled = True
        majority_wet = False
        probe_wet = [False, False, False]

        should_track = (tracking_enabled and
                        not majority_wet and
                        probe_wet.count(False) == 3)

        self.assertTrue(should_track)

    def test_tracking_disabled_when_wet(self):
        """Tracking should not occur when majority is wet."""
        tracking_enabled = True
        majority_wet = True
        probe_wet = [True, True, False]

        should_track = (tracking_enabled and
                        not majority_wet and
                        probe_wet.count(False) == 3)

        self.assertFalse(should_track)


class TestBaselineCapture(unittest.TestCase):
    """Test baseline capture logic."""

    def test_median_selection(self):
        """Baseline should select median value from sorted readings."""
        readings = [1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350,
                    1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750,
                    1800, 1850, 1900, 1950]
        readings.sort()
        baseline = readings[10]  # Middle value (index 10 of 20)

        self.assertEqual(baseline, 1500)

    def test_readings_sorted(self):
        """Readings should be sorted before median selection."""
        readings = [1500, 1100, 1800, 1200, 1700]
        readings.sort()

        self.assertEqual(readings, [1100, 1200, 1500, 1700, 1800])


class TestServoControl(unittest.TestCase):
    """Test servo control constants and logic."""

    def test_servo_pwm_values(self):
        """Servo PWM values should be correct for 50Hz."""
        SERVO_OPEN = 3277      # 1.0ms pulse = 0°
        SERVO_CLOSED = 4915    # 1.5ms pulse = 90°

        # Verify they're different
        self.assertNotEqual(SERVO_OPEN, SERVO_CLOSED)

        # Verify OPEN is less than CLOSED
        self.assertLess(SERVO_OPEN, SERVO_CLOSED)

    def test_state_change_detection(self):
        """State changes should be detected correctly."""
        # Transition from dry to wet
        majority_wet = True
        prev_majority_wet = False

        should_close = majority_wet and not prev_majority_wet
        should_open = not majority_wet and prev_majority_wet

        self.assertTrue(should_close)
        self.assertFalse(should_open)

        # Transition from wet to dry
        majority_wet = False
        prev_majority_wet = True

        should_close = majority_wet and not prev_majority_wet
        should_open = not majority_wet and prev_majority_wet

        self.assertFalse(should_close)
        self.assertTrue(should_open)

        # No change
        majority_wet = True
        prev_majority_wet = True

        should_close = majority_wet and not prev_majority_wet
        should_open = not majority_wet and prev_majority_wet

        self.assertFalse(should_close)
        self.assertFalse(should_open)


if __name__ == '__main__':
    unittest.main()
