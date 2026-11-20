import math
import unittest

from laser_turret.control.pid import ControlMode, JointCommand
from laser_turret.simulation.plant import TwoAxisPlant


def command(
    mode: ControlMode,
    pan: float,
    tilt: float,
    *,
    timestamp: float = 0.0,
    expiry: float = 10.0,
    sequence: int = 1,
) -> JointCommand:
    return JointCommand(
        sequence=sequence,
        timestamp_s=timestamp,
        expiry_s=expiry,
        mode=mode,
        pan_rad=pan,
        tilt_rad=tilt,
    )


class TwoAxisPlantTests(unittest.TestCase):
    def test_same_seed_produces_the_same_noisy_trajectory(self) -> None:
        left_truth, left_observed = self._run_noisy(seed=530)
        right_truth, right_observed = self._run_noisy(seed=530)
        other_truth, other_observed = self._run_noisy(seed=531)

        self.assertEqual(left_truth, right_truth)
        self.assertEqual(left_observed, right_observed)
        self.assertEqual(left_truth, other_truth)
        self.assertNotEqual(left_observed, other_observed)

    def test_joint_and_rate_limits_hold_for_an_aggressive_command(self) -> None:
        plant = TwoAxisPlant()
        demand = command(ControlMode.ACTIVE, pan=100.0, tilt=-100.0)
        previous_pan_rate = 0.0
        previous_tilt_rate = 0.0
        state = plant.step(demand, 0.0)
        for _ in range(400):
            state = plant.step(demand, 0.01)
            self.assertLessEqual(state.pan_rad, plant.pan_max_rad)
            self.assertGreaterEqual(state.pan_rad, plant.pan_min_rad)
            self.assertLessEqual(state.tilt_rad, plant.tilt_max_rad)
            self.assertGreaterEqual(state.tilt_rad, plant.tilt_min_rad)
            self.assertLessEqual(abs(state.pan_rate_rad_s), plant.max_rate_rad_s + 1e-12)
            self.assertLessEqual(abs(state.tilt_rate_rad_s), plant.max_rate_rad_s + 1e-12)
            self.assertLessEqual(
                abs(state.pan_rate_rad_s - previous_pan_rate),
                plant.max_accel_rad_s2 * 0.01 + 1e-9,
            )
            self.assertLessEqual(
                abs(state.tilt_rate_rad_s - previous_tilt_rate),
                plant.max_accel_rad_s2 * 0.01 + 1e-9,
            )
            previous_pan_rate = state.pan_rate_rad_s
            previous_tilt_rate = state.tilt_rate_rad_s

        self.assertTrue(state.pan_at_limit)
        self.assertTrue(state.tilt_at_limit)
        self.assertAlmostEqual(state.pan_rad, plant.pan_max_rad)
        self.assertAlmostEqual(state.tilt_rad, plant.tilt_min_rad)

    def test_expired_command_holds(self) -> None:
        plant = TwoAxisPlant()
        live = command(ControlMode.ACTIVE, pan=0.8, tilt=0.3, expiry=10.0)
        for _ in range(15):
            plant.step(live, 0.01)
        self.assertGreater(plant.pan_rate_rad_s, 0.0)
        position_when_expired = plant.pan_rad

        expired = command(
            ControlMode.ACTIVE,
            pan=2.0,
            tilt=2.0,
            expiry=plant.time_s - 1e-6,
        )
        state = plant.step(expired, 0.01)
        for _ in range(80):
            state = plant.step(expired, 0.01)

        self.assertEqual(state.applied_mode, ControlMode.HOLD)
        self.assertAlmostEqual(state.pan_rate_rad_s, 0.0, places=6)
        self.assertAlmostEqual(state.tilt_rate_rad_s, 0.0, places=6)
        self.assertGreaterEqual(state.pan_rad, position_when_expired)
        self.assertLess(state.pan_rad, 1.0)
        self.assertLess(state.tilt_rad, 0.5)

    def test_hold_from_rest_does_not_follow_the_command_position(self) -> None:
        plant = TwoAxisPlant()
        hold = command(ControlMode.HOLD, pan=1.0, tilt=-0.5)
        for _ in range(20):
            state = plant.step(hold, 0.01)
        self.assertEqual(state.pan_rad, 0.0)
        self.assertEqual(state.tilt_rad, 0.0)
        self.assertEqual(state.applied_mode, ControlMode.HOLD)

    def test_disabled_command_does_not_move_the_plant(self) -> None:
        plant = TwoAxisPlant(initial_pan_rad=0.2, initial_tilt_rad=-0.1)
        live = command(ControlMode.ACTIVE, pan=0.8, tilt=-0.4, expiry=10.0)
        for _ in range(10):
            plant.step(live, 0.01)
        self.assertNotEqual(plant.pan_rate_rad_s, 0.0)

        frozen_pan = plant.pan_rad
        frozen_tilt = plant.tilt_rad
        disabled = command(ControlMode.DISABLED, pan=1.2, tilt=0.6, expiry=10.0)
        state = plant.step(disabled, 0.01)
        later = plant.step(disabled, 0.05)

        self.assertEqual(state.pan_rad, frozen_pan)
        self.assertEqual(state.tilt_rad, frozen_tilt)
        self.assertEqual(later.pan_rad, frozen_pan)
        self.assertEqual(later.tilt_rad, frozen_tilt)
        self.assertEqual(later.pan_rate_rad_s, 0.0)
        self.assertEqual(later.tilt_rate_rad_s, 0.0)
        self.assertEqual(later.applied_mode, ControlMode.DISABLED)

    def test_negative_dt_is_rejected(self) -> None:
        plant = TwoAxisPlant()
        with self.assertRaises(ValueError):
            plant.step(command(ControlMode.HOLD, pan=0.0, tilt=0.0), -0.1)

    def _run_noisy(self, seed: int) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
        plant = TwoAxisPlant(seed=seed, observation_stddev_rad=0.01)
        demand = command(ControlMode.ACTIVE, pan=0.25, tilt=-0.15)
        truth: list[tuple[float, float]] = []
        observed: list[tuple[float, float]] = []
        for _ in range(30):
            plant.step(demand, 0.01)
            truth.append((plant.pan_rad, plant.tilt_rad))
            observed.append(plant.measure())
        self.assertTrue(all(math.isfinite(value) for sample in observed for value in sample))
        return truth, observed


if __name__ == "__main__":
    unittest.main()
