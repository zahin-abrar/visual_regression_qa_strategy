#!/usr/bin/env bash
# Disk diagnostics for the Android build workflow. Read-only; shallow `du` on known paths only.
# Usage: disk-report.sh <checkpoint label>
set -u
echo "=== DISK REPORT: ${1:-unlabelled} ==="
df -h / /mnt "${GITHUB_WORKSPACE:-.}" 2>&1 || true
echo "--- inodes ---"
df -i / "${GITHUB_WORKSPACE:-.}" 2>&1 || true
echo "--- free on build filesystem ($(df --output=target "${GITHUB_WORKSPACE:-.}" | tail -1)) ---"
df -h --output=avail "${GITHUB_WORKSPACE:-.}" | tail -1
echo "--- sizes (du -sh, existing paths only) ---"
for p in \
  "$HOME/.gradle" "$HOME/.android" "$HOME/.npm" "$HOME/.local/share/pnpm" \
  "${GITHUB_WORKSPACE:-.}/app/node_modules" "${GITHUB_WORKSPACE:-.}/app/android" \
  "${GITHUB_WORKSPACE:-.}/app/android/app/.cxx" "${GITHUB_WORKSPACE:-.}/app/android/app/build" \
  /usr/local/lib/android /opt/hostedtoolcache /usr/share/dotnet /opt/ghc /usr/local/.ghcup \
  /usr/local/share/boost /opt/hostedtoolcache/CodeQL /usr/share/swift /opt/microsoft /usr/local/share/powershell /var/lib/docker /tmp; do
  [ -e "$p" ] && du -sh "$p" 2>/dev/null
done
echo "=== END DISK REPORT: ${1:-unlabelled} ==="
exit 0
