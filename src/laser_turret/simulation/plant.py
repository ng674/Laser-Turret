"""Dependency-free two-axis pan/tilt plant.

The joint numbers below are provisional stand-ins. Mass, inertia, servo lag,
travel, and rate have not been measured on the delivered mechanism.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

from ..control.pid import ControlMode, JointCommand

# Provisional and unmeasured. Not limits of a delivered servo.
PROVISIONAL_PAN_MIN_RAD = -math.pi / 2
PROVISIONAL_PAN_MAX_RAD = math.pi / 2
PROVISIONAL_TILT_MIN_RAD = -math.pi / 4
PROVISIONAL_TILT_MAX_RAD = math.pi / 4
PROVISIONAL_MAX_RATE_RAD_S = math.pi
PROVISIONAL_MAX_ACCEL_RAD_S2 = 4.0 * math.pi
PROVISIONAL_ACTUATOR_LAG_S = 0.04
PROVISIONAL_TRACKING_TIME_S = 0.05


@dataclass(frozen=True, slots=True)
class PlantState:
    """True joint state after one step. Observation noise is not included."""

    time_s: float
    pan_rad: float
    tilt_rad: float
    pan_rate_rad_s: float
    tilt_rate_rad_s: float
    pan_at_limit: bool
    tilt_at_limit: bool
    applied_mode: ControlMode


def _clamp(value: float, low: float, high: float) -> float:
    return min(max(value, low), high)


class TwoAxisPlant:
    """Pan and tilt position/velocity with lag, rate caps, and soft limits."""

    def __init__(
        self,
        *,
        pan_min_rad: float = PROVISIONAL_PAN_MIN_RAD,
        pan_max_rad: float = PROVISIONAL_PAN_MAX_RAD,
        tilt_min_rad: float = PROVISIONAL_TILT_MIN_RAD,
        tilt_max_rad: float = PROVISIONAL_TILT_MAX_RAD,
        max_rate_rad_s: float = PROVISIONAL_MAX_RATE_RAD_S,
        max_accel_rad_s2: float = PROVISIONAL_MAX_ACCEL_RAD_S2,
        actuator_lag_s: float = PROVISIONAL_ACTUATOR_LAG_S,
        tracking_time_s: float = PROVISIONAL_TRACKING_TIME_S,
        observation_stddev_rad: float = 0.0,
        seed: int = 530,
        initial_pan_rad: float = 0.0,
        initial_tilt_rad: float = 0.0,
    ) -> None:
        if pan_min_rad >= pan_max_rad or tilt_min_rad >= tilt_max_rad:
            raise ValueError("joint limits must be ordered")
        if max_rate_rad_s <= 0.0 or max_accel_rad_s2 <= 0.0 or tracking_time_s <= 0.0:
            raise ValueError("rate, acceleration, and tracking time must be positive")
        if actuator_lag_s < 0.0 or observation_stddev_rad < 0.0:
            raise ValueError("lag and observation noise must be non-negative")
        if not math.isfinite(initial_pan_rad) or not math.isfinite(initial_tilt_rad):
            raise ValueError("initial joint positions must be finite")
        if not pan_min_rad <= initial_pan_rad <= pan_max_rad:
            raise ValueError("initial pan is outside the soft limits")
        if not tilt_min_rad <= initial_tilt_rad <= tilt_max_rad:
            raise ValueError("initial tilt is outside the soft limits")
        self.pan_min_rad = pan_min_rad
        self.pan_max_rad = pan_max_rad
        self.tilt_min_rad = tilt_min_rad
        self.tilt_max_rad = tilt_max_rad
        self.max_rate_rad_s = max_rate_rad_s
        self.max_accel_rad_s2 = max_accel_rad_s2
        self.actuator_lag_s = actuator_lag_s
        self.tracking_time_s = tracking_time_s
        self.observation_stddev_rad = observation_stddev_rad
        self.seed = seed
        self.time_s = 0.0
        self.pan_rad = initial_pan_rad
        self.tilt_rad = initial_tilt_rad
        self.pan_rate_rad_s = 0.0
        self.tilt_rate_rad_s = 0.0
        self._pan_lag = initial_pan_rad
        self._tilt_lag = initial_tilt_rad
        self._rng = random.Random(seed)

    def measure(self) -> tuple[float, float]:
        """Return pan and tilt with seeded observation noise."""

        if self.observation_stddev_rad == 0.0:
            return (self.pan_rad, self.tilt_rad)
        return (
            self.pan_rad + self._rng.gauss(0.0, self.observation_stddev_rad),
            self.tilt_rad + self._rng.gauss(0.0, self.observation_stddev_rad),
        )

    def step(self, command: JointCommand, dt: float) -> PlantState:
        """Advance one timestep. DISABLED freezes the joints."""

        if not math.isfinite(dt) or dt < 0.0:
            raise ValueError("dt must be a non-negative finite number")
        mode = self._effective_mode(command)
        if mode is ControlMode.DISABLED:
            self.pan_rate_rad_s = 0.0
            self.tilt_rate_rad_s = 0.0
            self._pan_lag = self.pan_rad
            self._tilt_lag = self.tilt_rad
        else:
            self.pan_rad, self.pan_rate_rad_s, self._pan_lag = self._track_axis(
                self.pan_rad,
                self.pan_rate_rad_s,
                self._pan_lag,
                command.pan_rad,
                self.pan_min_rad,
                self.pan_max_rad,
                dt,
                brake=mode is not ControlMode.ACTIVE,
            )
            self.tilt_rad, self.tilt_rate_rad_s, self._tilt_lag = self._track_axis(
                self.tilt_rad,
                self.tilt_rate_rad_s,
                self._tilt_lag,
                command.tilt_rad,
                self.tilt_min_rad,
                self.tilt_max_rad,
                dt,
                brake=mode is not ControlMode.ACTIVE,
            )
        self.time_s += dt
        return self._snapshot(mode)

    def _effective_mode(self, command: JointCommand) -> ControlMode:
        if command.mode is ControlMode.DISABLED:
            return ControlMode.DISABLED
        expired = self.time_s > command.expiry_s
        not_finite = not math.isfinite(command.pan_rad) or not math.isfinite(command.tilt_rad)
        if command.mode is not ControlMode.ACTIVE or expired or not_finite:
            return ControlMode.HOLD
        return ControlMode.ACTIVE

    def _track_axis(
        self,
        position: float,
        rate: float,
        lag: float,
        target: float,
        low: float,
        high: float,
        dt: float,
        *,
        brake: bool,
    ) -> tuple[float, float, float]:
        if brake:
            desired_rate = 0.0
            lag = position
        else:
            target = _clamp(target, low, high)
            if self.actuator_lag_s <= 0.0:
                alpha = 1.0
            else:
                alpha = 1.0 - math.exp(-dt / self.actuator_lag_s)
            lag = lag + alpha * (target - lag)
            desired_rate = _clamp(
                (lag - position) / self.tracking_time_s,
                -self.max_rate_rad_s,
                self.max_rate_rad_s,
            )
        room_high = max(0.0, high - position)
        room_low = max(0.0, position - low)
        safe_high = math.sqrt(2.0 * self.max_accel_rad_s2 * room_high)
        safe_low = math.sqrt(2.0 * self.max_accel_rad_s2 * room_low)
        desired_rate = _clamp(
            desired_rate,
            -min(self.max_rate_rad_s, safe_low),
            min(self.max_rate_rad_s, safe_high),
        )
        max_delta = self.max_accel_rad_s2 * dt
        rate_delta = _clamp(desired_rate - rate, -max_delta, max_delta)
        rate = _clamp(rate + rate_delta, -self.max_rate_rad_s, self.max_rate_rad_s)
        position = position + rate * dt
        if position > high or high - position <= 1e-12:
            position = high
        elif position < low or position - low <= 1e-12:
            position = low
        return position, rate, lag

    def _snapshot(self, mode: ControlMode) -> PlantState:
        return PlantState(
            time_s=self.time_s,
            pan_rad=self.pan_rad,
            tilt_rad=self.tilt_rad,
            pan_rate_rad_s=self.pan_rate_rad_s,
            tilt_rate_rad_s=self.tilt_rate_rad_s,
            pan_at_limit=self.pan_rad <= self.pan_min_rad or self.pan_rad >= self.pan_max_rad,
            tilt_at_limit=self.tilt_rad <= self.tilt_min_rad or self.tilt_rad >= self.tilt_max_rad,
            applied_mode=mode,
        )
