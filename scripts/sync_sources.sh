#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ROOT/sources"

sync_repo() {
  local name="$1"
  local url="$2"
  local dest="$ROOT/sources/$name"

  if [[ -d "$dest/.git" ]]; then
    git -C "$dest" fetch --quiet origin
    git -C "$dest" checkout --quiet main
    git -C "$dest" pull --ff-only --quiet origin main
  else
    git clone --quiet --depth 1 "$url" "$dest"
  fi
}

sync_repo healthcare-ai-data-engineer https://github.com/anix-lynch/healthcare-ai-data-engineer.git
sync_repo healthcare-da https://github.com/anix-lynch/healthcare-da.git
sync_repo healthcare-signal-platform https://github.com/anix-lynch/healthcare-signal-platform.git
sync_repo healthcare-genai-engineer https://github.com/anix-lynch/healthcare-genai-engineer.git

echo "Baymax sibling sources are synced."
