"""Checks for the simplified MuJoCo turret. Skipped when MuJoCo is not installed."""

from __future__ import annotations

import math
import unittest
from pathlib import Path

try:
    import mujoco
except ImportError:  # standard-library test runs must pass without MuJoCo
    mujoco = None

MODEL_PATH = Path(__file__).resolve().parents[1] / "simulation" / "mujoco" / "turret.xml"


@unittest.skipIf(mujoco is None, "mujoco is not installed; run make setup-sim")
class TurretModelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
        self.data = mujoco.MjData(self.model)

    def settle(self, pan_rad: float, tilt_rad: float, seconds: float = 1.0) -> None:
        self.data.ctrl[:] = (pan_rad, tilt_rad)
        for _ in range(int(seconds / self.model.opt.timestep)):
            mujoco.mj_step(self.model, self.data)

    def test_exactly_two_actuated_hinges(self) -> None:
        self.assertEqual(self.model.njnt, 2)
        self.assertEqual(self.model.nu, 2)
        for name in ("pan", "tilt"):
            joint = self.model.joint(name)
            self.assertEqual(joint.type[0], mujoco.mjtJoint.mjJNT_HINGE)
            self.assertEqual(self.model.actuator(name).trnid[0], joint.id)

    def test_joint_axes_and_parents(self) -> None:
        self.assertEqual(list(self.model.joint("pan").axis), [0.0, 0.0, 1.0])
        self.assertEqual(list(self.model.joint("tilt").axis), [1.0, 0.0, 0.0])
        tilt_parent = self.model.body("tilt").parentid[0]
        self.assertEqual(tilt_parent, self.model.body("pan").id)

    def test_camera_is_fixed_to_base(self) -> None:
        camera = self.model.camera("base_camera")
        self.assertEqual(camera.bodyid[0], self.model.body("base").id)

    def test_zero_pose_aims_along_negative_y(self) -> None:
        self.settle(0.0, 0.0)
        tilt_body = self.data.body("tilt")
        aim_world = tilt_body.xmat.reshape(3, 3) @ (0.0, -1.0, 0.0)
        self.assertAlmostEqual(aim_world[1], -1.0, places=3)

    def test_head_tracks_command(self) -> None:
        self.settle(0.35, 0.07)
        self.assertAlmostEqual(self.data.joint("pan").qpos[0], 0.35, delta=0.01)
        self.assertAlmostEqual(self.data.joint("tilt").qpos[0], 0.07, delta=0.01)
        self.assertTrue(all(self.data.warning[i].number == 0 for i in range(len(self.data.warning))))

    def test_control_range_limits_commands(self) -> None:
        self.settle(10.0, -10.0)
        self.assertLessEqual(self.data.joint("pan").qpos[0], math.pi / 2 + 0.01)
        self.assertGreaterEqual(self.data.joint("tilt").qpos[0], -math.pi / 4 - 0.01)


if __name__ == "__main__":
    unittest.main()
