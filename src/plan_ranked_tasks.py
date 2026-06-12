#!/usr/bin/env python3
"""Plan ranked SandScout tasks for future real-agent evaluation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_tasks(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "tasks" in data:
        return data["tasks"]
    if isinstance(data, list):
        return data
    raise ValueError("expected task list or object with tasks")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--top-k", type=int, default=7)
    args = parser.parse_args()

    tasks = load_tasks(args.tasks)
    ranked = sorted(
        tasks,
        key=lambda task: (
            -task.get("confidence", 0.0),
            task["surface"],
            task.get("repo", ""),
            task["id"],
        ),
    )
    high_confidence = [task for task in ranked if task.get("confidence", 0.0) >= 0.75]
    readme_only = [task for task in ranked if task.get("source_files") == ["README.md"]]

    surface_seen = set()
    balanced = []
    for task in ranked:
        if task["surface"] in surface_seen:
            continue
        balanced.append(task)
        surface_seen.add(task["surface"])

    result = {
        "top_k": args.top_k,
        "ranked_top_k": ranked[: args.top_k],
        "high_confidence_count": len(high_confidence),
        "readme_only_control_count": len(readme_only),
        "surface_balanced_queue": balanced,
        "recommended_live_queue": [
            task for task in ranked if task.get("confidence", 0.0) >= 0.75 and task.get("source_files") != ["README.md"]
        ][: args.top_k],
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
