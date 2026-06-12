#!/usr/bin/env python3
"""Create a safe synthetic repository corpus for SandScout mining tests."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


FIXTURES = {
    "node_package_agent": {
        "package.json": '{"name":"node-package-agent","scripts":{"test":"echo ok"}}\n',
        "README.md": "# Node package fixture\n",
    },
    "python_tooling_agent": {
        "pyproject.toml": "[project]\nname = \"python-tooling-agent\"\nversion = \"0.1.0\"\n",
        "AGENTS.md": "# Agent notes\nUse project-local instructions when editing metadata.\n",
    },
    "devcontainer_startup": {
        ".devcontainer/devcontainer.json": '{"name":"devcontainer-startup","image":"python:3.12"}\n',
        ".vscode/settings.json": '{"python.testing.pytestEnabled": true}\n',
        "README.md": "# Devcontainer startup fixture\n",
    },
    "ci_workflow_agent": {
        ".github/workflows/test.yml": "name: test\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo ok\n",
        "README.md": "# CI workflow fixture\n",
    },
    "tool_manifest_agent": {
        ".mcp.json": '{"mcpServers":{}}\n',
        ".cursor/mcp.json": '{"mcpServers":{}}\n',
        "README.md": "# Tool manifest fixture\n",
    },
    "low_signal_docs": {
        "README.md": "# Documentation-only fixture\nThis repository intentionally has minimal metadata.\n",
        "docs/usage.md": "# Usage\nNo lifecycle configuration here.\n",
    },
}


def write_fixture(root: Path, name: str, files: dict[str, str]) -> None:
    repo = root / name
    repo.mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()

    if args.clean and args.out.exists():
        shutil.rmtree(args.out)
    args.out.mkdir(parents=True, exist_ok=True)

    for name, files in FIXTURES.items():
        write_fixture(args.out, name, files)

    print(f"wrote {len(FIXTURES)} fixtures to {args.out}")


if __name__ == "__main__":
    main()
