import unittest

from laser_turret.tracking import ConstantVelocityKalman2D


class ConstantVelocityKalmanTests(unittest.TestCase):
    def test_filter_learns_positive_velocity_and_reduces_noise(self) -> None:
        kf = ConstantVelocityKalman2D(
            0.0, 0.0, process_variance=1.0, measurement_variance=4.0
        )
        raw_errors = []
        filtered_errors = []
        for step in range(1, 31):
            truth = float(step)
            measurement = truth + (2.0 if step % 2 else -2.0)
            kf.predict(0.1)
            x, _ = kf.update(measurement, 0.0)
            raw_errors.append(abs(measurement - truth))
            filtered_errors.append(abs(x - truth))
        self.assertGreater(kf.velocity[0], 0.0)
        self.assertLess(sum(filtered_errors) / len(filtered_errors), sum(raw_errors) / len(raw_errors))

    def test_negative_time_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ConstantVelocityKalman2D(0.0, 0.0).predict(-0.1)


if __name__ == "__main__":
    unittest.main()

