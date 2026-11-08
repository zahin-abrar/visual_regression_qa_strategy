#!/usr/bin/env bash
# Install the one runtime library the Android emulator binary needs but the hosted Ubuntu 24.04
# image lacks (libpulse.so.0 -> package libpulse0). Bounded; any failure is a real failure.
set -euo pipefail
if ldconfig -p | grep -q 'libpulse\.so\.0'; then
  echo "libpulse.so.0 already resolvable"
else
  sudo timeout 180 apt-get update -o Acquire::Retries=1
  sudo timeout 300 env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends libpulse0
fi
ldconfig -p | grep 'libpulse\.so\.0' || { echo "::error title=libpulse missing::libpulse.so.0 still not resolvable after installing libpulse0"; exit 1; }
