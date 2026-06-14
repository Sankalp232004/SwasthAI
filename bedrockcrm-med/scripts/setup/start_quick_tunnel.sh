#!/bin/bash
set -euo pipefail

# Start a free temporary public URL for local app via Cloudflare Tunnel.
# Usage: bash scripts/setup/start_quick_tunnel.sh [local_port]

PORT="${1:-5010}"

if ! command -v cloudflared >/dev/null 2>&1; then
  echo "cloudflared is not installed."
  echo "Install on macOS: brew install cloudflared"
  echo "Then rerun: bash scripts/setup/start_quick_tunnel.sh ${PORT}"
  exit 1
fi

echo "Starting Cloudflare quick tunnel to http://127.0.0.1:${PORT}"
echo "Keep this terminal open while sharing your app URL."

auto_url=$(cloudflared tunnel --url "http://127.0.0.1:${PORT}" 2>&1 | tee /tmp/swasthai_tunnel.log | grep -Eo 'https://[-a-z0-9]+\.trycloudflare\.com' | head -n1 || true)

if [[ -n "$auto_url" ]]; then
  echo "Public URL: $auto_url"
else
  echo "Tunnel started. If URL not shown above, check /tmp/swasthai_tunnel.log"
fi
