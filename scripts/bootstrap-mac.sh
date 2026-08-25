#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME_DIR="$ROOT_DIR/runtime"

echo "OH Ventures Mac bootstrap"
echo "========================="

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "This bootstrap is intended for macOS."
  exit 1
fi

if [[ "$(uname -m)" != "arm64" ]]; then
  echo "Warning: target architecture is Apple Silicon arm64."
fi

if ! xcode-select -p >/dev/null 2>&1; then
  echo "Xcode Command Line Tools are missing."
  echo "Run: xcode-select --install"
  exit 1
fi

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew is missing. Install it from https://brew.sh then rerun this script."
  exit 1
fi

brew install git uv jq >/dev/null

if ! command -v ollama >/dev/null 2>&1; then
  echo "Installing Ollama..."
  brew install --cask ollama
fi

if ! command -v hermes >/dev/null 2>&1; then
  echo "Hermes is not installed yet."
  echo "Use the current official Nous Research Hermes installer, then rerun this script."
  echo "The installer URL can change, so this script deliberately does not curl|bash a moving remote target automatically."
fi

cd "$RUNTIME_DIR"

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created runtime/.env from template. Add secrets before enabling live connectors."
fi

uv sync
uv run ohv init

echo
echo "Bootstrap complete."
echo "Next commands:"
echo "  cd $RUNTIME_DIR"
echo "  uv run ohv health"
echo "  uv run ohv demo-signal"
echo
echo "Keep OHV_SHADOW_MODE=true until agent calibration is complete."
