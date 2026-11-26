"""Снимок метрик Python по исходникам, radon и фактическому coverage.xml."""

import argparse
import json
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from pathlib import Path

from radon.complexity import cc_visit
from radon.raw import analyze

LAB_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = LAB_DIR.parents[1]

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--coverage", type=Path, default=REPO_ROOT / "artifacts/python/coverage.xml")
parser.add_argument("--output", type=Path, default=LAB_DIR / "evidence/metrics.json")
args = parser.parse_args()
root = ET.parse(args.coverage).getroot()
modules = {}
for source in (REPO_ROOT / "TestingPS/Laba-1/delivery.py", LAB_DIR / "calculator.py"):
    filename = source.name
    text = source.read_text()
    raw = analyze(text)
    coverage = next(c for c in root.iter("class") if Path(c.attrib["filename"]).name == filename)
    modules[filename] = {
        "loc": raw.loc,
        "sloc": raw.sloc,
        "comments": raw.comments,
        "complexity": {block.name: block.complexity for block in cc_visit(text)},
        "line_coverage_percent": float(coverage.attrib["line-rate"]) * 100,
        "branch_coverage_percent": float(coverage.attrib["branch-rate"]) * 100,
        "confirmed_local_defects": 0,
        "defect_density_per_kloc": 0.0,
        "reaction_time_ms": None,
    }
report = {
    "generated_utc": datetime.now(UTC).isoformat(),
    "modules": modules,
    "defect_note": "0 найденных дефектов не доказывает их отсутствие; риски см. отчёты.",
    "loc_definition": "radon raw LOC: все строки; SLOC: строки кода без комментариев/docstring",
}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(report, ensure_ascii=False, indent=2))
