"""Блокирующий gate для JSON npm audit: ошибки формата тоже завершаются ошибкой."""

import argparse
import json
from pathlib import Path


def check(report: dict) -> int:
    if "error" in report:
        raise ValueError(f"npm audit failed: {report['error']}")
    counts = report["metadata"]["vulnerabilities"]
    critical = counts["critical"]
    if not isinstance(critical, int) or isinstance(critical, bool) or critical < 0:
        raise ValueError("invalid critical vulnerability count")
    print(f"npm audit: critical={critical}, high={counts.get('high', 'unknown')}")
    return int(critical > 0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    raise SystemExit(check(json.loads(args.report.read_text())))
