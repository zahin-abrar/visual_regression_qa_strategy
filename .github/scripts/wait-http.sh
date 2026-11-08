#!/usr/bin/env bash
# wait-http.sh <name> <url> <timeout-seconds> [grep-pattern] : bounded readiness check.
set -u
name=$1; url=$2; limit=$3; pat=${4:-}
deadline=$(( $(date +%s) + limit ))
while :; do
  if body=$(curl -fsS --max-time 5 "$url" 2>/dev/null); then
    if [ -z "$pat" ] || printf '%s' "$body" | grep -q "$pat"; then
      echo "$name ready: $url"
      exit 0
    fi
  fi
  if [ "$(date +%s)" -ge "$deadline" ]; then
    echo "::error title=$name not ready::no healthy response from $url within ${limit}s"
    exit 1
  fi
  sleep 3
done
