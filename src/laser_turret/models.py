from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Detection:
    """One detector observation in image pixel coordinates."""

    timestamp_s: float
    frame_id: int
    label: str
    confidence: float
    x: float
    y: float
    width: float = 0.0
    height: float = 0.0


@dataclass(frozen=True, slots=True)
class TrackSnapshot:
    """Public, immutable view of a track after filtering."""

    track_id: int
    timestamp_s: float
    label: str
    x: float
    y: float
    vx: float
    vy: float
    position_variance: float
    age: int
    hits: int
    misses: int
    confirmed: bool

