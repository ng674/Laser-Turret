import math
import unittest

from laser_turret.control.pid import (
    BoundedPID,
    ControlMode,
    DesiredBearing,
    bearing_from_degrees,
    degrees_to_radians,
)
from laser_turret.simulation.plant import (
    PROVISIONAL_MAX_RATE_RAD_S,
    PROVISIONAL_PAN_MAX_RAD,
    PROVISIONAL_PAN_MIN_RAD,
    PROVISIONAL_TILT_MAX_RAD,
    PROVISIONAL_TILT_MIN_RAD,
    TwoAxisPlant,
)


class BoundedPIDTests(unittest.TestCase):
    def test_degree_conversion_is_explicit(self) -> None:
        bearing = bearing_from_degrees(timestamp_s=1.25, pan_deg=20.0, tilt_deg=4.0)

        self.assertAlmostEqual(bearing.pan_rad, degrees_to_radians(20.0))
        self.assertAlmostEqual(bearing.pan_rad, math.radians(20.0))
        self.assertAlmostEqual(bearing.tilt_rad, degrees_to_radians(4.0))
        self.assertTrue(bearing.valid)

    def test_default_limits_match_the_provisional_plant(self) -> None:
        controller = BoundedPID()

        self.assertEqual(controller.pan_min_rad, PROVISIONAL_PAN_MIN_RAD)
        self.assertEqual(controller.pan_max_rad, PROVISIONAL_PAN_MAX_RAD)
        self.assertEqual(controller.tilt_min_rad, PROVISIONAL_TILT_MIN_RAD)
        self.assertEqual(controller.tilt_max_rad, PROVISIONAL_TILT_MAX_RAD)
        self.assertEqual(controller.max_rate_rad_s, PROVISIONAL_MAX_RATE_RAD_S)
        self.assertEqual(controller.mode, ControlMode.DISABLED)

    def test_invalid_bearing_enters_hold(self) -> None:
        controller = BoundedPID()
        controller.set_mode(ControlMode.ACTIVE)
        invalid = DesiredBearing(timestamp_s=0.0, pan_rad=0.4, tilt_rad=-0.2, valid=False)
        not_finite = DesiredBearing(timestamp_s=0.0, pan_rad=math.nan, tilt_rad=0.0, valid=True)

        invalid_command = controller.update(invalid, 0.1, -0.05, 0.0)
        missing_command = controller.update(None, 0.1, -0.05, 0.01)
        controller.set_mode(ControlMode.ACTIVE)
        nan_command = controller.update(not_finite, 0.1, -0.05, 0.02)

        self.assertEqual(invalid_command.mode, ControlMode.HOLD)
        self.assertEqual(missing_command.mode, ControlMode.HOLD)
        self.assertEqual(nan_command.mode, ControlMode.HOLD)
        self.assertAlmostEqual(invalid_command.pan_rad, 0.1)
        self.assertAlmostEqual(nan_command.tilt_rad, -0.05)

    def test_stale_bearing_enters_hold(self) -> None:
        controller = BoundedPID()
        controller.set_mode(ControlMode.ACTIVE)
        stale = bearing_from_degrees(timestamp_s=0.0, pan_deg=20.0, tilt_deg=4.0)

        command = controller.update(stale, 0.0, 0.0, now_s=controller.stale_after_s + 0.01)

        self.assertEqual(command.mode, ControlMode.HOLD)
        self.assertEqual(controller.pan_integral_rad, 0.0)

    def test_disabled_mode_ignores_a_fresh_bearing(self) -> None:
        controller = BoundedPID()
        bearing = bearing_from_degrees(timestamp_s=0.0, pan_deg=20.0, tilt_deg=4.0)

        command = controller.update(bearing, 0.2, -0.1, 0.0)

        self.assertEqual(command.mode, ControlMode.DISABLED)
        self.assertAlmostEqual(command.pan_rad, 0.2)
        self.assertAlmostEqual(command.tilt_rad, -0.1)

    def test_disabled_output_does_not_move_the_plant(self) -> None:
        plant = TwoAxisPlant()
        controller = BoundedPID()
        bearing = bearing_from_degrees(timestamp_s=0.0, pan_deg=20.0, tilt_deg=4.0)
        command = controller.update(bearing, plant.pan_rad, plant.tilt_rad, 0.0)
        state = plant.step(command, 0.01)

        self.assertEqual(state.pan_rad, 0.0)
        self.assertEqual(state.tilt_rad, 0.0)
        self.assertEqual(state.applied_mode, ControlMode.DISABLED)

    def test_active_command_is_clamped_to_provisional_limits(self) -> None:
        controller = BoundedPID(
            kp=1.0,
            ki=0.0,
            kd=0.0,
            max_rate_rad_s=100.0,
            command_lifetime_s=1.0,
        )
        controller.set_mode(ControlMode.ACTIVE)
        bearing = DesiredBearing(timestamp_s=0.0, pan_rad=10.0, tilt_rad=-10.0, valid=True)

        command = controller.update(bearing, 0.0, 0.0, 0.0)

        self.assertEqual(command.mode, ControlMode.ACTIVE)
        self.assertAlmostEqual(command.pan_rad, controller.pan_max_rad)
        self.assertAlmostEqual(command.tilt_rad, controller.tilt_min_rad)
        self.assertGreater(command.expiry_s, command.timestamp_s)

    def test_integral_is_clamped(self) -> None:
        controller = BoundedPID(
            kp=0.0,
            ki=1.0,
            kd=0.0,
            integral_limit_rad=0.2,
            max_rate_rad_s=100.0,
            command_lifetime_s=1.0,
        )
        controller.set_mode(ControlMode.ACTIVE)
        for step in range(100):
            now = step * 0.05
            bearing = DesiredBearing(timestamp_s=now, pan_rad=0.05, tilt_rad=-0.05, valid=True)
            controller.update(bearing, 0.0, 0.0, now)

        self.assertAlmostEqual(controller.pan_integral_rad, 0.2)
        self.assertAlmostEqual(controller.tilt_integral_rad, -0.2)

    def test_scripted_bearing_settles_without_growing_oscillation(self) -> None:
        plant = TwoAxisPlant(observation_stddev_rad=0.0)
        controller = BoundedPID()
        controller.set_mode(ControlMode.ACTIVE)
        dt = 0.01
        pan_error: list[float] = []
        tilt_error: list[float] = []
        target_pan = degrees_to_radians(20.0)
        target_tilt = degrees_to_radians(4.0)

        for step in range(300):
            now = step * dt
            bearing = bearing_from_degrees(timestamp_s=now, pan_deg=20.0, tilt_deg=4.0)
            command = controller.update(bearing, plant.pan_rad, plant.tilt_rad, now)
            self.assertEqual(command.mode, ControlMode.ACTIVE)
            state = plant.step(command, dt)
            self.assertLessEqual(abs(state.pan_rate_rad_s), plant.max_rate_rad_s + 1e-12)
            self.assertLessEqual(abs(state.tilt_rate_rad_s), plant.max_rate_rad_s + 1e-12)
            self.assertLessEqual(state.pan_rad, plant.pan_max_rad + 1e-12)
            self.assertGreaterEqual(state.tilt_rad, plant.tilt_min_rad - 1e-12)
            pan_error.append(state.pan_rad - target_pan)
            tilt_error.append(state.tilt_rad - target_tilt)

        self.assertLess(self._peak(pan_error, 200, 300), self._peak(pan_error, 0, 50))
        self.assertLess(self._peak(tilt_error, 200, 300), self._peak(tilt_error, 0, 50))
        self.assertLess(abs(pan_error[-1]), 0.02)
        self.assertLess(abs(tilt_error[-1]), 0.02)
        self.assertLess(abs(plant.pan_rate_rad_s), 0.05)
        self.assertLess(abs(plant.tilt_rate_rad_s), 0.05)

    @staticmethod
    def _peak(values: list[float], start: int, end: int) -> float:
        return max(abs(value) for value in values[start:end])


if __name__ == "__main__":
    unittest.main()
