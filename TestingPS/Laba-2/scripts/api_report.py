"""Публикует только безопасную сводку Newman, без токенов и полных сетевых дампов."""

import json
from datetime import UTC, datetime
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = LAB_DIR.parents[1]
EVIDENCE_DIR = LAB_DIR / "evidence"
EVIDENCE_DIR.mkdir(exist_ok=True)
raw = json.loads((REPO_ROOT / "artifacts/api/run.json").read_text())
cases = {c["id"]: c for c in json.loads((LAB_DIR / "postman/cases.json").read_text())}
rows = []
for execution in raw["run"]["executions"]:
    case_id = execution["item"]["name"].split()[0]
    response = execution.get("response") or {}
    failed = [a["assertion"] for a in execution.get("assertions", []) if a.get("error")]
    rows.append(
        {
            **cases[case_id],
            "actual_status": response.get("code"),
            "response_time_ms": response.get("responseTime"),
            "failed_checks": failed,
            "result": "FAIL" if failed or execution.get("requestError") else "PASS",
        }
    )
report = {
    "generated_utc": datetime.now(UTC).isoformat(),
    "stats": raw["run"]["stats"],
    "cases": rows,
}
(EVIDENCE_DIR / "api-results.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n"
)
table = [
    "# Фактические результаты API",
    "",
    "Источник: реальный Newman; секреты исключены.",
    "",
    "| ID | Запрос | Тип | Ожидалось | Получено | мс | Статус |",
    "|---|---|---|---|---|---|---|",
]
for r in rows:
    table.append(
        f"| {r['id']} | {r['method']} {r['path']} | {r['category']} | "
        f"{r['expected_status']} | {r['actual_status']} | "
        f"{r['response_time_ms']} | {r['result']} |"
    )
(EVIDENCE_DIR / "api-results.md").write_text("\n".join(table) + "\n")
print(f"Saved {len(rows)} sanitized results")
