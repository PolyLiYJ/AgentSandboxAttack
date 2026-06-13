#!/usr/bin/env python3
"""Detect unsafe content classes in SandScout tasks and run artifacts.

The scanner is intentionally conservative. It flags risky evidence for review
without printing or expanding exploit details. SandScout still uses benign
sentinels for evaluation; this module helps prove the artifact stays clean.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RiskRule:
    category: str
    pattern: re.Pattern[str]
    severity: str
    description: str


RULES = (
    RiskRule(
        "credential_or_secret",
        re.compile(
            r"(?i)\b("
            r"api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token|"
            r"private[_-]?key|password|passwd|bearer\s+[a-z0-9._~+/=-]{12,}"
            r")\b"
        ),
        "high",
        "Credential, secret, token, or private-key indicator.",
    ),
    RiskRule(
        "destructive_command",
        re.compile(
            r"(?i)("
            r"rm\s+-[^\n;|&]*r[^\n;|&]*\s+[/~$]|"
            r"mkfs(?:\.[a-z0-9]+)?\s+|"
            r"dd\s+if=.*\s+of=/dev/|"
            r"chmod\s+777\s+/|"
            r"chown\s+-R\s+[^ \n]+\s+/"
            r")"
        ),
        "high",
        "Potentially destructive filesystem or device command.",
    ),
    RiskRule(
        "real_exploit_payload",
        re.compile(
            r"(?i)\b("
            r"reverse\s+shell|bind\s+shell|meterpreter|msfvenom|"
            r"shellcode|payload\s*=\s*|/bin/sh\s+-i|"
            r"curl\s+[^;\n|&]*\|\s*(?:sh|bash)|wget\s+[^;\n|&]*\|\s*(?:sh|bash)"
            r")\b"
        ),
        "high",
        "Exploit-payload or shell-staging indicator.",
    ),
    RiskRule(
        "product_specific_vulnerability_claim",
        re.compile(
            r"(?i)\b("
            r"CVE-\d{4}-\d{4,7}|0day|zero-day|"
            r"vulnerab(?:le|ility)\s+in\s+[A-Z][A-Za-z0-9_. -]{2,}|"
            r"bypass\s+(?:for|in)\s+[A-Z][A-Za-z0-9_. -]{2,}"
            r")\b"
        ),
        "medium",
        "Product-specific vulnerability or bypass claim.",
    ),
)


def redact(value: str, limit: int = 96) -> str:
    snippet = " ".join(value.strip().split())
    if len(snippet) > limit:
        snippet = snippet[: limit - 3] + "..."
    return snippet


def line_for_span(text: str, start: int, end: int) -> str:
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end == -1:
        line_end = len(text)
    return text[line_start:line_end]


def is_negated_safety_instruction(category: str, line: str) -> bool:
    lowered = line.lower()
    if "do not" not in lowered and "must not" not in lowered and "never" not in lowered:
        return False
    if category == "credential_or_secret" and any(term in lowered for term in ("credential", "secret", "token", "password")):
        return True
    if category == "real_exploit_payload" and any(term in lowered for term in ("payload", "shell", "malware")):
        return True
    if category == "destructive_command" and "destructive" in lowered:
        return True
    return False


def scan_text(text: str, source: str) -> list[dict]:
    findings: list[dict] = []
    for rule in RULES:
        for match in rule.pattern.finditer(text):
            line = line_for_span(text, match.start(), match.end())
            if is_negated_safety_instruction(rule.category, line):
                continue
            findings.append(
                {
                    "source": source,
                    "category": rule.category,
                    "severity": rule.severity,
                    "description": rule.description,
                    "span": [match.start(), match.end()],
                    "excerpt": redact(match.group(0)),
                }
            )
    return findings


def scan_files(paths: list[Path]) -> list[dict]:
    findings: list[dict] = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        findings.extend(scan_text(text, str(path)))
    return findings


def summarize(findings: list[dict]) -> dict:
    categories = sorted({finding["category"] for finding in findings})
    severities = sorted({finding["severity"] for finding in findings})
    return {
        "finding_count": len(findings),
        "categories": categories,
        "severities": severities,
        "clean": len(findings) == 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    findings = scan_files(args.paths)
    result = {"summary": summarize(findings), "findings": findings}
    text = json.dumps(result, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
