#!/usr/bin/env python3
"""Generate the SandScout real-agent control matrix figure as dependency-free SVG."""

from __future__ import annotations

import csv
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "paper" / "results" / "real_agent_control_matrix.csv"
OUT_DIR = ROOT / "paper" / "figures"
OUT = OUT_DIR / "fig_control_matrix.svg"


SURFACE_LABELS = {
    "tool_manifest_discovery": "Tool manifest",
    "package_lifecycle_config": "Package lifecycle",
    "startup_runtime_discovery": "Startup/runtime",
    "ci_workflow_transition": "CI workflow",
}

COLORS = {
    "positive": "#2A9D8F",
    "zero": "#E9C46A",
    "pending": "#B8B8C8",
    "ink": "#17202A",
    "muted": "#4B5563",
    "grid": "#E5E7EB",
    "bg": "#FFFFFF",
}


def load_rows() -> list[dict[str, str]]:
    with DATA.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def rect(x: int, y: int, w: int, h: int, fill: str, rx: int = 10) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="#FFFFFF" stroke-width="2"/>'
    )


def text(x: int, y: int, body: str, size: int = 13, weight: str = "400", anchor: str = "middle", color: str = COLORS["ink"]) -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="Times New Roman, DejaVu Serif, serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}">'
        f'{escape(body)}</text>'
    )


def cell(x: int, y: int, fill: str, main: str, sub: str) -> list[str]:
    return [
        rect(x, y, 128, 62, fill),
        text(x + 64, y + 28, main, size=15, weight="700"),
        text(x + 64, y + 47, sub, size=10, color=COLORS["ink"]),
    ]


def main() -> None:
    rows = load_rows()
    width = 760
    height = 310
    left = 150
    top = 86
    col_w = 142
    row_h = 76

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="{COLORS["bg"]}"/>',
        text(width // 2, 32, "SandScout real-agent SSE-SR by boundary surface", size=18, weight="700"),
        text(width // 2, 54, "Matched no-note controls omit SandScout repository context", size=12, color=COLORS["muted"]),
    ]

    parts.append(text(88, top + 38, "Mined context", size=13, weight="700"))
    parts.append(text(88, top + row_h + 38, "No-note control", size=13, weight="700"))

    for i, row in enumerate(rows):
        x = left + i * col_w
        label = SURFACE_LABELS[row["surface"]]
        parts.append(text(x + 64, top - 18, label, size=12, weight="700"))

        parts.extend(cell(x, top, COLORS["positive"], f"{float(row['positive_sse_sr']):.2f}", row["positive_run"]))
        if row["control_status"] == "complete":
            parts.extend(cell(x, top + row_h, COLORS["zero"], f"{float(row['control_sse_sr']):.2f}", row["control_run"]))
        else:
            parts.extend(cell(x, top + row_h, COLORS["pending"], "pending", "usage limit"))

    legend_y = 252
    legend = [
        ("Sentinel created", COLORS["positive"]),
        ("No sentinel", COLORS["zero"]),
        ("Pending", COLORS["pending"]),
    ]
    for i, (label, color) in enumerate(legend):
        x = 180 + i * 170
        parts.append(rect(x, legend_y - 13, 20, 20, color, rx=4))
        parts.append(text(x + 30, legend_y + 2, label, size=11, anchor="start", color=COLORS["muted"]))

    caption = "Cells show SSE-SR. Pending denotes a usage-limit availability failure, not model behavior."
    parts.append(text(width // 2, 292, caption, size=11, color=COLORS["muted"]))
    parts.append("</svg>")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
