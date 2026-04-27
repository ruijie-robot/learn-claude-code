#!/usr/bin/env bash
set -euo pipefail

# Hook contract (s08_hook_system.py teaching version):
# - Exit 0: allow
# - Exit 1: block (reason in stderr)
#
# s08 passes tool context via env:
# - HOOK_TOOL_NAME
# - HOOK_TOOL_INPUT (JSON, contains {"command": "..."} for Bash tool)

tool_name="${HOOK_TOOL_NAME:-}"
tool_input="${HOOK_TOOL_INPUT:-}"

# Only gate Bash tool invocations.
if [[ -n "$tool_name" && "$tool_name" != "Bash" ]]; then
  exit 0
fi

cmd="$(
  python3 - <<'PY'
import json, os, sys
raw = os.environ.get("HOOK_TOOL_INPUT", "") or ""
try:
    data = json.loads(raw) if raw.strip() else {}
except Exception:
    data = {}
cmd = data.get("command", "")
if not isinstance(cmd, str):
    cmd = ""
sys.stdout.write(cmd)
PY
)"

# Empty command -> allow.
if [[ -z "${cmd//[[:space:]]/}" ]]; then
  exit 0
fi

# Very conservative deny-list. Adjust as you learn.
danger_patterns=(
  "rm -rf /"
  "rm -rf /*"
  "mkfs"
  "dd if="
  "diskutil erase"
  "shutdown"
  "reboot"
  "halt"
  ":(){"
)

for p in "${danger_patterns[@]}"; do
  if [[ "$cmd" == *"$p"* ]]; then
    echo "Blocked dangerous shell command (matched: $p)" 1>&2
    echo "Command: $cmd" 1>&2
    exit 1
  fi
done

exit 0
