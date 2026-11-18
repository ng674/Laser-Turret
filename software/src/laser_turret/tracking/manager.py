from __future__ import annotations

from dataclasses import dataclass
from math import hypot

from laser_turret.models import Detection, TrackSnapshot

from .kalman import ConstantVelocityKalman2D


@dataclass(frozen=True, slots=True)
class TrackerConfig:
    process_variance: float = 30.0
    measurement_variance: float = 16.0
    association_distance_px: float = 90.0
    minimum_confirmed_hits: int = 3
    maximum_missed_frames: int = 8


@dataclass(slots=True)
class _Track:
    track_id: int
    label: str
    filter: ConstantVelocityKalman2D
    timestamp_s: float
    age: int = 1
    hits: int = 1
    misses: int = 0


class MultiObjectTracker:
    """Greedy nearest-neighbor association plus one Kalman filter per object."""

    def __init__(self, config: TrackerConfig | None = None) -> None:
        self.config = config or TrackerConfig()
        self._tracks: dict[int, _Track] = {}
        self._next_id = 1

    def _new_track(self, detection: Detection) -> None:
        kalman = ConstantVelocityKalman2D(
            detection.x,
            detection.y,
            process_variance=self.config.process_variance,
            measurement_variance=self.config.measurement_variance,
        )
        self._tracks[self._next_id] = _Track(
            track_id=self._next_id,
            label=detection.label,
            filter=kalman,
            timestamp_s=detection.timestamp_s,
        )
        self._next_id += 1

    def update(self, detections: list[Detection], timestamp_s: float) -> list[TrackSnapshot]:
        if any(d.timestamp_s != timestamp_s for d in detections):
            raise ValueError("all detection timestamps must match the update timestamp")

        for track in self._tracks.values():
            dt = timestamp_s - track.timestamp_s
            if dt < 0.0:
                raise ValueError("timestamps must be monotonic")
            track.filter.predict(dt)
            track.timestamp_s = timestamp_s
            track.age += 1

        candidates: list[tuple[float, int, int]] = []
        for track_id, track in self._tracks.items():
            tx, ty = track.filter.position
            for detection_index, detection in enumerate(detections):
                if detection.label != track.label:
                    continue
                distance = hypot(detection.x - tx, detection.y - ty)
                if distance <= self.config.association_distance_px:
                    candidates.append((distance, track_id, detection_index))
        candidates.sort()

        matched_tracks: set[int] = set()
        matched_detections: set[int] = set()
        for _, track_id, detection_index in candidates:
            if track_id in matched_tracks or detection_index in matched_detections:
                continue
            detection = detections[detection_index]
            track = self._tracks[track_id]
            track.filter.update(detection.x, detection.y)
            track.hits += 1
            track.misses = 0
            matched_tracks.add(track_id)
            matched_detections.add(detection_index)

        for track_id, track in self._tracks.items():
            if track_id not in matched_tracks:
                track.misses += 1
        for index, detection in enumerate(detections):
            if index not in matched_detections:
                self._new_track(detection)

        expired = [
            track_id
            for track_id, track in self._tracks.items()
            if track.misses > self.config.maximum_missed_frames
        ]
        for track_id in expired:
            del self._tracks[track_id]

        return self.snapshots()

    def snapshots(self) -> list[TrackSnapshot]:
        snapshots: list[TrackSnapshot] = []
        for track in sorted(self._tracks.values(), key=lambda item: item.track_id):
            x, y = track.filter.position
            vx, vy = track.filter.velocity
            snapshots.append(
                TrackSnapshot(
                    track_id=track.track_id,
                    timestamp_s=track.timestamp_s,
                    label=track.label,
                    x=x,
                    y=y,
                    vx=vx,
                    vy=vy,
                    position_variance=track.filter.position_variance,
                    age=track.age,
                    hits=track.hits,
                    misses=track.misses,
                    confirmed=track.hits >= self.config.minimum_confirmed_hits,
                )
            )
        return snapshots

