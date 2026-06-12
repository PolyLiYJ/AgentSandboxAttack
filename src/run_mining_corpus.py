#!/usr/bin/env python3
"""Run SandScout mining over a directory of repositories."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from sandscout_miner import mine


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    repos = sorted(path for path in args.corpus.iterdir() if path.is_dir())
    rows = []
    all_tasks = []
    for repo in repos:
        tasks = mine(repo)
        surface_counts = Counter(task["surface"] for task in tasks)
        rows.append(
            {
                "repo": repo.name,
                "task_count": len(tasks),
                "surfaces": dict(sorted(surface_counts.items())),
            }
        )
        for index, task in enumerate(tasks, start=1):
            task = dict(task)
            task["local_id"] = task["id"]
            task["id"] = f"{repo.name}_{index:03d}_{task['surface']}"
            task["repo"] = repo.name
            all_tasks.append(task)

    surface_totals = Counter(task["surface"] for task in all_tasks)
    high_confidence = [task for task in all_tasks if task.get("confidence", 0.0) >= 0.75]
    result = {
        "repo_count": len(repos),
        "task_count": len(all_tasks),
        "high_confidence_task_count": len(high_confidence),
        "surface_totals": dict(sorted(surface_totals.items())),
        "repos": rows,
        "tasks": all_tasks,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
