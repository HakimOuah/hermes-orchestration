#!/usr/bin/env bash
set -euo pipefail

pass=0
warn=0

check_cmd() {
  local cmd="$1"
  local label="$2"
  if command -v "$cmd" >/dev/null 2>&1; then
    printf "[ok]   %-24s %s\n" "$label" "$(command -v "$cmd")"
    pass=$((pass+1))
  else
    printf "[warn] %-24s missing\n" "$label"
    warn=$((warn+1))
  fi
}

echo "OH Ventures Mac prerequisite check"
echo "----------------------------------"
printf "macOS: %s\n" "$(sw_vers -productVersion 2>/dev/null || echo unknown)"
printf "arch:  %s\n\n" "$(uname -m)"

check_cmd git "Git"
check_cmd brew "Homebrew"
check_cmd uv "uv"
check_cmd hermes "Hermes"
check_cmd ollama "Ollama"
check_cmd docker "Docker (optional)"
check_cmd node "Node.js"
check_cmd rg "ripgrep"
check_cmd ffmpeg "ffmpeg"

if command -v curl >/dev/null 2>&1 && curl -fsS --max-time 2 http://127.0.0.1:11434 >/dev/null 2>&1; then
  echo "[ok]   Local inference         reachable on :11434"
else
  echo "[warn] Local inference         not reachable on :11434"
fi

printf "\nSummary: %d available, %d warnings\n" "$pass" "$warn"
echo "Warnings are expected before the Mac bootstrap is completed."
