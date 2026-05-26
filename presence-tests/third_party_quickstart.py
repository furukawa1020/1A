#!/usr/bin/env python3
"""Run the README-style third-party quickstart commands."""

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


COMMANDS = [
    ["python", "presence-audit/cli/presence_audit.py", "audit", "templates/self_observation_local_only/presence.yaml", "--fail-on", "HIGH"],
    ["python", "presence-audit/cli/presence_audit.py", "scan", "templates/self_observation_local_only", "--fail-on", "HIGH"],
    ["python", "presence-audit/cli/presence_audit.py", "audit", "templates/local_assertive_to_non_assertive_migration/before.presence.yaml"],
    ["python", "presence-audit/cli/presence_audit.py", "audit", "templates/local_assertive_to_non_assertive_migration/after.presence.yaml", "--fail-on", "HIGH"],
    ["python", "presence-bench/run_benchmark.py", "--output", "presence-bench/reports/benchmark_report.md", "--json-output", "presence-bench/reports/benchmark_report.json"],
]


def main():
    rows = []
    for command in COMMANDS:
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        rows.append(
            {
                "command": command,
                "returncode": completed.returncode,
                "stdout_tail": completed.stdout[-600:],
                "stderr_tail": completed.stderr[-600:],
            }
        )
        if completed.returncode != 0:
            output = {"passed": False, "rows": rows}
            print(json.dumps(output, ensure_ascii=False, indent=2))
            return completed.returncode
    output = {"passed": True, "rows": rows}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
