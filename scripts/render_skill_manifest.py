#!/usr/bin/env python3
"""Render a simple index of skill files."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    skills = sorted(ROOT.glob("skills/**/SKILL.md"))
    for skill in skills:
        print(skill.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

