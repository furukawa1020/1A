#!/usr/bin/env python3
"""Standalone PRESENCE Guard micro-benchmark."""

import argparse
import json
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "presence-audit" / "cli"))

import presence_audit as pa  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=50000)
    parser.add_argument("--output", default=str(ROOT / "analysis" / "outputs" / "presence_overhead.json"))
    args = parser.parse_args(argv)

    policy = pa.load_json(ROOT / "presence-policy" / "presence.guard.policy.json")
    requests = [
        pa.load_json(ROOT / "presence-tests" / "fixtures" / "request_soft_cue_self.json"),
        pa.load_json(ROOT / "presence-tests" / "fixtures" / "request_high_stress_self.json"),
        pa.load_json(ROOT / "presence-tests" / "fixtures" / "request_productivity_manager.json"),
    ]

    start = time.perf_counter()
    counts = {"allow": 0, "rewrite": 0, "deny": 0}
    for index in range(args.iterations):
        decision = pa.guard_decision(policy, requests[index % len(requests)])
        counts[decision["decision"]] += 1
    elapsed = time.perf_counter() - start
    result = {
        "iterations": args.iterations,
        "total_seconds": elapsed,
        "mean_decision_latency_ms": (elapsed / args.iterations) * 1000,
        "decisions": counts,
        "policy_size_bytes": len(json.dumps(policy, ensure_ascii=False).encode("utf-8")),
        "engine": "presence-audit Python reference engine",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
