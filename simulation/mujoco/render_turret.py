"""Render the simplified V8 turret MJCF to PNG files, headless.

Usage (from the repository root):

    .venv/bin/python simulation/mujoco/render_turret.py
    .venv/bin/python simulation/mujoco/render_turret.py --pan-deg 30 --tilt-deg -15

Writes an overview image and a view from the fixed base camera for each pose to
runs/mujoco/ (git-ignored). Images are for inspecting geometry and pointing only;
the base camera uses a placeholder field of view, not a calibrated one.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import mujoco
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = REPO_ROOT / "simulation" / "mujoco" / "turret.xml"
DEFAULT_OUTPUT = REPO_ROOT / "runs" / "mujoco"
DEFAULT_POSES_DEG = ((0.0, 0.0), (45.0, 0.0), (-30.0, 20.0), (20.0, -30.0))
SETTLE_S = 1.0


def settle(model: mujoco.MjModel, data: mujoco.MjData, pan_rad: float, tilt_rad: float) -> None:
    """Command both position actuators and step until the head settles."""

    data.ctrl[model.actuator("pan").id] = pan_rad
    data.ctrl[model.actuator("tilt").id] = tilt_rad
    for _ in range(int(SETTLE_S / model.opt.timestep)):
        mujoco.mj_step(model, data)


def overview_camera() -> mujoco.MjvCamera:
    camera = mujoco.MjvCamera()
    camera.lookat[:] = (0.03, -0.05, 0.08)
    camera.distance = 0.55
    camera.azimuth = -125.0
    camera.elevation = -22.0
    return camera


def save_png(path: Path, pixels: np.ndarray) -> None:
    """Write an RGB uint8 array as PNG without third-party image libraries."""

    import struct
    import zlib

    height, width, _ = pixels.shape
    raw = b"".join(b"\x00" + pixels[row].tobytes() for row in range(height))

    def chunk(tag: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + tag + body + struct.pack(">I", zlib.crc32(tag + body))

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(raw, 6))
        + chunk(b"IEND", b"")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pan-deg", type=float, help="single pose: pan angle in degrees")
    parser.add_argument("--tilt-deg", type=float, default=0.0, help="single pose: tilt in degrees")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--width", type=int, default=960)
    parser.add_argument("--height", type=int, default=720)
    args = parser.parse_args()

    poses = DEFAULT_POSES_DEG if args.pan_deg is None else ((args.pan_deg, args.tilt_deg),)
    args.output.mkdir(parents=True, exist_ok=True)

    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)
    with mujoco.Renderer(model, height=args.height, width=args.width) as renderer:
        for pan_deg, tilt_deg in poses:
            settle(model, data, math.radians(pan_deg), math.radians(tilt_deg))
            tag = f"pan{pan_deg:+04.0f}_tilt{tilt_deg:+04.0f}"
            for view, camera in (("overview", overview_camera()), ("base_camera", "base_camera")):
                renderer.update_scene(data, camera=camera)
                path = args.output / f"{tag}_{view}.png"
                save_png(path, renderer.render())
                print(path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path)
            pan, tilt = (math.degrees(v) for v in data.qpos[:2])
            print(f"  settled pan={pan:.2f} deg tilt={tilt:.2f} deg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
