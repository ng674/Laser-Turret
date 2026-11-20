"""Bounded pan/tilt controller for simulation only.

Angles are radians. Positive pan is to the right and positive tilt is up.
Nothing in this module talks to hardware or an optical source.
"""

from __future__ import annotations

import enum
import math
from dataclasses import dataclass


class ControlMode(enum.Enum):
    """Explicit actuator permission. The safe default is DISABLED."""

    DISABLED = "DISABLED"
    HOLD = "HOLD"
    ACTIVE = "ACTIVE"


@dataclass(frozen=True, slots=True)
class DesiredBearing:
    """One aim sample in joint radians, not image pixels."""

    timestamp_s: float
    pan_rad: float
    tilt_rad: float
    valid: bool = True


@dataclass(frozen=True, slots=True)
class JointCommand:
    """Position command the simulated plant is allowed to consume."""

    sequence: int
    timestamp_s: float
    expiry_s: float
    mode: ControlMode
    pan_rad: float
    tilt_rad: float


def degrees_to_radians(degrees: float) -> float:
    """Convert one explicit degree value into radians."""

    return degrees * math.pi / 180.0


def bearing_from_degrees(
    *,
    timestamp_s: float,
    pan_deg: float,
    tilt_deg: float,
    valid: bool = True,
) -> DesiredBearing:
    """Build a bearing from a degree aim.

    Positive pan is to the right. Positive tilt is up. This is the only
    degree-to-radian conversion on the control boundary.
    """

    return DesiredBearing(
        timestamp_s=timestamp_s,
        pan_rad=degrees_to_radians(pan_deg),
        tilt_rad=degrees_to_radians(tilt_deg),
        valid=valid,
    )


def _clamp(value: float, low: float, high: float) -> float:
    return min(max(value, low), high)


class BoundedPID:
    """Pan/tilt PID with disabled, hold, and active modes.

    Default joint bounds match the provisional constants on ``TwoAxisPlant``.
    Those bounds are unmeasured stand-ins, not delivered-servo limits.
    """

    def __init__(
        self,
        *,
        kp: float = 1.0,
        ki: float = 0.15,
        kd: float = 0.01,
        integral_limit_rad: float = 0.4,
        max_rate_rad_s: float = math.pi,
        pan_min_rad: float = -math.pi / 2,
        pan_max_rad: float = math.pi / 2,
        tilt_min_rad: float = -math.pi / 4,
        tilt_max_rad: float = math.pi / 4,
        stale_after_s: float = 0.150,
        command_lifetime_s: float = 0.050,
    ) -> None:
        if pan_min_rad >= pan_max_rad or tilt_min_rad >= tilt_max_rad:
            raise ValueError("joint limits must be ordered")
        if max_rate_rad_s <= 0.0 or integral_limit_rad < 0.0 or command_lifetime_s <= 0.0:
            raise ValueError("rate, integral limit, and command lifetime must be positive")
        if stale_after_s < 0.0:
            raise ValueError("stale_after_s must be non-negative")
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral_limit_rad = integral_limit_rad
        self.max_rate_rad_s = max_rate_rad_s
        self.pan_min_rad = pan_min_rad
        self.pan_max_rad = pan_max_rad
        self.tilt_min_rad = tilt_min_rad
        self.tilt_max_rad = tilt_max_rad
        self.stale_after_s = stale_after_s
        self.command_lifetime_s = command_lifetime_s
        self.mode = ControlMode.DISABLED
        self.pan_integral_rad = 0.0
        self.tilt_integral_rad = 0.0
        self._previous_pan_error = 0.0
        self._previous_tilt_error = 0.0
        self._has_previous = False
        self._last_now_s: float | None = None
        self._sequence = 0

    def set_mode(self, mode: ControlMode) -> None:
        if not isinstance(mode, ControlMode):
            raise TypeError("mode must be a ControlMode")
        self.mode = mode
        if mode is not ControlMode.ACTIVE:
            self._reset_memory()

    def update(
        self,
        bearing: DesiredBearing | None,
        measured_pan_rad: float,
        measured_tilt_rad: float,
        now_s: float,
    ) -> JointCommand:
        """Return the next command. Invalid or stale bearings become HOLD."""

        if not math.isfinite(now_s):
            raise ValueError("now_s must be finite")
        if self._last_now_s is None:
            dt = 0.0
        else:
            dt = now_s - self._last_now_s
            if dt < 0.0:
                raise ValueError("now_s must be non-decreasing")
        self._last_now_s = now_s

        mode = self._resolve_mode(bearing, now_s)
        if mode is not ControlMode.ACTIVE or bearing is None:
            self._reset_memory()
            return self._command(mode, now_s, measured_pan_rad, measured_tilt_rad)

        pan_command, self.pan_integral_rad, pan_error = self._control_axis(
            bearing.pan_rad,
            measured_pan_rad,
            self.pan_integral_rad,
            self._previous_pan_error,
            dt,
            self.pan_min_rad,
            self.pan_max_rad,
        )
        tilt_command, self.tilt_integral_rad, tilt_error = self._control_axis(
            bearing.tilt_rad,
            measured_tilt_rad,
            self.tilt_integral_rad,
            self._previous_tilt_error,
            dt,
            self.tilt_min_rad,
            self.tilt_max_rad,
        )
        self._previous_pan_error = pan_error
        self._previous_tilt_error = tilt_error
        self._has_previous = True
        return self._command(ControlMode.ACTIVE, now_s, pan_command, tilt_command)

    def _resolve_mode(self, bearing: DesiredBearing | None, now_s: float) -> ControlMode:
        if self.mode is ControlMode.DISABLED:
            return ControlMode.DISABLED
        fresh = bearing is not None and self._bearing_is_fresh(bearing, now_s)
        if self.mode is ControlMode.HOLD or not fresh:
            return ControlMode.HOLD
        return ControlMode.ACTIVE

    def _bearing_is_fresh(self, bearing: DesiredBearing, now_s: float) -> bool:
        if not bearing.valid:
            return False
        if not math.isfinite(bearing.timestamp_s):
            return False
        if not math.isfinite(bearing.pan_rad) or not math.isfinite(bearing.tilt_rad):
            return False
        return now_s - bearing.timestamp_s <= self.stale_after_s

    def _control_axis(
        self,
        target: float,
        measured: float,
        integral: float,
        previous_error: float,
        dt: float,
        low: float,
        high: float,
    ) -> tuple[float, float, float]:
        error = _clamp(target, low, high) - measured
        updated_integral = _clamp(
            integral + error * dt,
            -self.integral_limit_rad,
            self.integral_limit_rad,
        )
        derivative = 0.0
        if self._has_previous and dt > 0.0:
            derivative = (error - previous_error) / dt
        raw = self.kp * error + self.ki * updated_integral + self.kd * derivative
        max_step = self.max_rate_rad_s * max(self.command_lifetime_s, dt)
        correction = _clamp(raw, -max_step, max_step)
        if correction != raw and error * (updated_integral - integral) > 0.0:
            updated_integral = integral
            raw = self.kp * error + self.ki * updated_integral + self.kd * derivative
            correction = _clamp(raw, -max_step, max_step)
        unlimited = measured + correction
        commanded = _clamp(unlimited, low, high)
        if commanded != unlimited and error * updated_integral > 0.0:
            updated_integral = integral
        return commanded, updated_integral, error

    def _command(
        self,
        mode: ControlMode,
        now_s: float,
        pan_rad: float,
        tilt_rad: float,
    ) -> JointCommand:
        self._sequence += 1
        return JointCommand(
            sequence=self._sequence,
            timestamp_s=now_s,
            expiry_s=now_s + self.command_lifetime_s,
            mode=mode,
            pan_rad=_clamp(pan_rad, self.pan_min_rad, self.pan_max_rad),
            tilt_rad=_clamp(tilt_rad, self.tilt_min_rad, self.tilt_max_rad),
        )

    def _reset_memory(self) -> None:
        self.pan_integral_rad = 0.0
        self.tilt_integral_rad = 0.0
        self._previous_pan_error = 0.0
        self._previous_tilt_error = 0.0
        self._has_previous = False
