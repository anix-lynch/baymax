#!/usr/bin/env bash
set -euo pipefail

base_url="${1:-https://baymax-bice.vercel.app}"
base_url="${base_url%/}"
page="$(mktemp)"
trap 'rm -f "$page"' EXIT

check_200() {
  local url="$1"
  local output="${2:-/dev/null}"
  local status
  status="$(curl --silent --show-error --location --output "$output" --write-out '%{http_code}' "$url")"
  if [[ "$status" != "200" ]]; then
    echo "public check failed: $url returned HTTP $status" >&2
    exit 1
  fi
}

check_200 "$base_url/" "$page"
check_200 "$base_url/outputs/baymax_audit.json"
check_200 "$base_url/outputs/deployment_readiness_receipt.json"

grep -q "What did Baymax find that nobody mentioned?" "$page" || {
  echo "public check failed: English showroom marker is missing" >&2
  exit 1
}

if python3 - "$page" <<'PY'
import pathlib
import sys

page = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
raise SystemExit(0 if any("\u0e00" <= char <= "\u0e7f" for char in page) else 1)
PY
then
  echo "public check failed: Thai UI copy remains in the public showroom" >&2
  exit 1
fi

echo "public showroom verified: $base_url/"
