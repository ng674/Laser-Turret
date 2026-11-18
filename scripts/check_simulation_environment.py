from __future__ import annotations

import importlib
import platform
import sys


REQUIRED_MODULES = ("mujoco", "gymnasium", "pytest")


def module_version(module_name: str) -> str:
    module = importlib.import_module(module_name)
    return str(getattr(module, "__version__", "installed (version not exposed)"))


def main() -> int:
    print(f"Python: {platform.python_version()} ({sys.executable})")
    failures: list[str] = []
    for module_name in REQUIRED_MODULES:
        try:
            version = module_version(module_name)
        except Exception as error:  # environment doctor must report every missing dependency
            failures.append(f"{module_name}: {error}")
        else:
            print(f"{module_name}: {version}")

    if failures:
        print("Simulation environment is incomplete:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        print("Run: make setup-sim", file=sys.stderr)
        return 1

    print("Simulation Python dependencies are available.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
