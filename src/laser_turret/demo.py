from __future__ import annotations

from laser_turret.models import Detection
from laser_turret.tracking import MultiObjectTracker


def main() -> None:
    tracker = MultiObjectTracker()
    print("frame  id  confirmed       x       y      vx      vy  misses")
    for frame_id in range(12):
        timestamp = frame_id / 30.0
        # Deterministic alternating measurement error around a moving object.
        noise = 2.0 if frame_id % 2 == 0 else -2.0
        detections = [] if frame_id == 7 else [
            Detection(timestamp, frame_id, "ball", 0.95, 100.0 + 5.0 * frame_id + noise, 200.0)
        ]
        for track in tracker.update(detections, timestamp):
            print(
                f"{frame_id:5d} {track.track_id:3d} {str(track.confirmed):>10} "
                f"{track.x:7.2f} {track.y:7.2f} {track.vx:7.2f} {track.vy:7.2f} "
                f"{track.misses:7d}"
            )


if __name__ == "__main__":
    main()

