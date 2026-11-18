import unittest

from laser_turret.models import Detection
from laser_turret.tracking import MultiObjectTracker, TrackerConfig


class MultiObjectTrackerTests(unittest.TestCase):
    def test_track_is_confirmed_and_survives_one_missing_detection(self) -> None:
        tracker = MultiObjectTracker(
            TrackerConfig(minimum_confirmed_hits=3, maximum_missed_frames=2)
        )
        track_id = None
        for frame in range(3):
            timestamp = frame * 0.1
            snapshots = tracker.update(
                [Detection(timestamp, frame, "ball", 0.9, 10.0 + frame, 20.0)], timestamp
            )
            track_id = snapshots[0].track_id
        self.assertTrue(snapshots[0].confirmed)

        snapshots = tracker.update([], 0.3)
        self.assertEqual(snapshots[0].track_id, track_id)
        self.assertEqual(snapshots[0].misses, 1)

    def test_different_labels_are_not_associated(self) -> None:
        tracker = MultiObjectTracker()
        tracker.update([Detection(0.0, 0, "ball", 0.9, 10.0, 10.0)], 0.0)
        snapshots = tracker.update([Detection(0.1, 1, "cup", 0.9, 10.0, 10.0)], 0.1)
        self.assertEqual({snapshot.label for snapshot in snapshots}, {"ball", "cup"})

    def test_expired_track_is_removed(self) -> None:
        tracker = MultiObjectTracker(TrackerConfig(maximum_missed_frames=1))
        tracker.update([Detection(0.0, 0, "ball", 0.9, 10.0, 10.0)], 0.0)
        tracker.update([], 0.1)
        self.assertEqual(tracker.update([], 0.2), [])


if __name__ == "__main__":
    unittest.main()

