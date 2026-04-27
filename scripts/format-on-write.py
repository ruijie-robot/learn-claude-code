#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path


def _parse_tool_input() -> dict:
    raw = os.environ.get("HOOK_TOOL_INPUT", "") or ""
    try:
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}
    return data if isinstance(data, dict) else {}


def _rewrite_text_file(path: Path) -> bool:
    try:
        original = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    except Exception:
        return False

    lines = original.splitlines()
    lines = [ln.rstrip() for ln in lines]
    new = "\n".join(lines) + "\n"

    if new == original:
        return False

    try:
        path.write_text(new, encoding="utf-8")
    except Exception:
        return False
    return True


def main() -> int:
    tool_name = os.environ.get("HOOK_TOOL_NAME", "")
    if tool_name and tool_name != "Write":
        return 0

    tool_input = _parse_tool_input()
    p = tool_input.get("path")
    if not isinstance(p, str) or not p.strip():
        return 0

    path = Path(p)
    if not path.exists() or not path.is_file():
        return 0

    changed = _rewrite_text_file(path)
    if changed:
        print(f"formatted: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
