from __future__ import annotations


class ConstantVelocityKalman2D:
    """Small dependency-free Kalman filter for [x, y, vx, vy]."""

    def __init__(
        self,
        x: float,
        y: float,
        *,
        process_variance: float = 30.0,
        measurement_variance: float = 16.0,
    ) -> None:
        self.state = [x, y, 0.0, 0.0]
        self.covariance = [
            [measurement_variance, 0.0, 0.0, 0.0],
            [0.0, measurement_variance, 0.0, 0.0],
            [0.0, 0.0, 100.0, 0.0],
            [0.0, 0.0, 0.0, 100.0],
        ]
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance

    @staticmethod
    def _matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
        return [
            [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))
        ]

    @staticmethod
    def _transpose(a: list[list[float]]) -> list[list[float]]:
        return [list(row) for row in zip(*a)]

    def predict(self, dt: float) -> tuple[float, float]:
        if dt < 0.0:
            raise ValueError("dt must be non-negative")
        f = [
            [1.0, 0.0, dt, 0.0],
            [0.0, 1.0, 0.0, dt],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
        self.state = [sum(f[i][j] * self.state[j] for j in range(4)) for i in range(4)]
        fp = self._matmul(f, self.covariance)
        predicted = self._matmul(fp, self._transpose(f))

        # White-acceleration process model.
        q = self.process_variance
        dt2, dt3, dt4 = dt * dt, dt * dt * dt, dt * dt * dt * dt
        process_noise = [
            [dt4 * q / 4.0, 0.0, dt3 * q / 2.0, 0.0],
            [0.0, dt4 * q / 4.0, 0.0, dt3 * q / 2.0],
            [dt3 * q / 2.0, 0.0, dt2 * q, 0.0],
            [0.0, dt3 * q / 2.0, 0.0, dt2 * q],
        ]
        self.covariance = [
            [predicted[i][j] + process_noise[i][j] for j in range(4)] for i in range(4)
        ]
        return self.state[0], self.state[1]

    def update(self, measured_x: float, measured_y: float) -> tuple[float, float]:
        # H selects x and y. The 2x2 innovation covariance is inverted directly.
        p = self.covariance
        r = self.measurement_variance
        s00, s01 = p[0][0] + r, p[0][1]
        s10, s11 = p[1][0], p[1][1] + r
        determinant = s00 * s11 - s01 * s10
        if abs(determinant) < 1e-12:
            raise ArithmeticError("singular innovation covariance")
        inv_s = [[s11 / determinant, -s01 / determinant], [-s10 / determinant, s00 / determinant]]

        ph_t = [[p[i][0], p[i][1]] for i in range(4)]
        gain = self._matmul(ph_t, inv_s)
        innovation = [measured_x - self.state[0], measured_y - self.state[1]]
        self.state = [
            self.state[i] + gain[i][0] * innovation[0] + gain[i][1] * innovation[1]
            for i in range(4)
        ]

        # Joseph form protects covariance symmetry/positivity better than (I-KH)P.
        i_minus_kh = [
            [float(i == j) - (gain[i][0] if j == 0 else gain[i][1] if j == 1 else 0.0)
             for j in range(4)]
            for i in range(4)
        ]
        left = self._matmul(i_minus_kh, p)
        joseph = self._matmul(left, self._transpose(i_minus_kh))
        krk_t = [
            [r * (gain[i][0] * gain[j][0] + gain[i][1] * gain[j][1]) for j in range(4)]
            for i in range(4)
        ]
        self.covariance = [
            [joseph[i][j] + krk_t[i][j] for j in range(4)] for i in range(4)
        ]
        return self.state[0], self.state[1]

    @property
    def position(self) -> tuple[float, float]:
        return self.state[0], self.state[1]

    @property
    def velocity(self) -> tuple[float, float]:
        return self.state[2], self.state[3]

    @property
    def position_variance(self) -> float:
        return 0.5 * (self.covariance[0][0] + self.covariance[1][1])

