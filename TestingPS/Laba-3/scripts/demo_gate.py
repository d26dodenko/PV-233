"""Опциональная инъекция отказа в CI. Применяется только через workflow_dispatch/variable."""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run_demo(mode: str) -> int:
    """Возвращает ненулевой код настоящего инструмента для выбранного сценария."""
    with tempfile.TemporaryDirectory(prefix="moroz-gate-") as directory:
        root = Path(directory)
        (root / "pytest.ini").write_text("[pytest]\naddopts = -p no:cacheprovider\n")
        if mode == "unit":
            (root / "test_failure.py").write_text("def test_gate():\n    assert 2 + 2 == 5\n")
            command = [
                sys.executable,
                "-m",
                "pytest",
                "-c",
                str(root / "pytest.ini"),
                "-v",
                str(root),
            ]
        elif mode == "coverage":
            (root / "example.py").write_text(
                "def classify(x):\n    if x > 0:\n        return 1\n    return 0\n"
            )
            (root / "test_example.py").write_text(
                "from example import classify\ndef test_positive():\n    assert classify(1) == 1\n"
            )
            command = [
                sys.executable,
                "-m",
                "pytest",
                "-c",
                str(root / "pytest.ini"),
                str(root),
                "--cov=example",
                "--cov-branch",
                "--cov-config=/dev/null",
                "--cov-fail-under=80",
                "--cov-report=term-missing",
            ]
        elif mode == "security":
            # Изолированный учебный fixture: не устанавливает уязвимую зависимость.
            (root / "unsafe.py").write_text(
                "import subprocess\ndef execute(user_input):\n"
                "    return subprocess.run(user_input, shell=True, check=True)\n"
            )
            command = [sys.executable, "-m", "bandit", "-lll", str(root / "unsafe.py")]
        elif mode == "none":
            return 0
        else:
            raise ValueError(f"unknown mode: {mode}")
        result = subprocess.run(command, cwd=root, check=False)  # noqa: S603
        print(json.dumps({"demo": mode, "tool_exit_code": result.returncode}), flush=True)
        if result.returncode == 0:
            raise RuntimeError("gate fixture unexpectedly passed")
        return result.returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["none", "unit", "coverage", "security"])
    raise SystemExit(run_demo(parser.parse_args().mode))
