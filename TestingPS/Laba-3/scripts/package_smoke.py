"""Упаковать release и проверить HTTP после извлечения в отдельный каталог."""

import json
import os
import subprocess
import tarfile
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parents[3]
archive = root / "artifacts/moroz-shop-linux-x64.tar.gz"
archive.parent.mkdir(parents=True, exist_ok=True)
with tarfile.open(archive, "w:gz") as tar:
    for name in ["target/release/moroz-shop", "TestingPS/Laba-3/frontend/dist"]:
        tar.add(root / name, arcname=name)
with tempfile.TemporaryDirectory(prefix="moroz-release-") as directory:
    with tarfile.open(archive) as tar:
        tar.extractall(directory, filter="data")
    environment = {**os.environ, "SHOP_ADDR": "127.0.0.1:3001"}
    process = subprocess.Popen(
        [str(Path(directory) / "target/release/moroz-shop")],
        cwd=directory,
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    try:
        for _ in range(50):
            try:
                with urllib.request.urlopen("http://127.0.0.1:3001/api/health", timeout=2):
                    break
            except OSError:
                if process.poll() is not None:
                    raise RuntimeError("release process stopped before ready") from None
                time.sleep(0.1)
        else:
            raise TimeoutError("release server was not ready in 5 seconds")
        checks = {}
        for path in ["/api/health", "/api/products", "/", "/products", "/signup"]:
            with urllib.request.urlopen("http://127.0.0.1:3001" + path, timeout=2) as response:
                body = response.read().decode()
                if response.status != 200:
                    raise RuntimeError(f"{path}: expected HTTP 200, got {response.status}")
                if not path.startswith("/api") and "<title>Moroz Store</title>" not in body:
                    raise RuntimeError(f"{path}: frontend index missing")
                checks[path] = {"status": response.status, "bytes": len(body)}
        report = {"archive": str(archive.relative_to(root)), "extracted_package_checks": checks}
        output = root / "TestingPS/Laba-3/evidence/package-smoke.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report, indent=2))
    finally:
        process.terminate()
        process.wait(timeout=5)
