#!/usr/bin/env bash
# Best-effort final diagnostics. Every external command is time-limited, output goes to files
# (never command substitution, so an adb daemon cannot hold a pipe open), and the script always
# exits 0 so it can never mask the original failure. Overrides for tests: ADB, DIAG_TIMEOUT, DISK_TIMEOUT.
set -u
: "${LOG_DIR:?LOG_DIR not set}"
ADB=${ADB:-adb}
T=${DIAG_TIMEOUT:-10}
DT=${DISK_TIMEOUT:-90}
mkdir -p "$LOG_DIR"
out="$LOG_DIR/logcat-tail.txt"

timeout -k 2 "$T" "$ADB" devices > "$LOG_DIR/adb-devices-final.txt" 2>&1 < /dev/null
rc=$?
if [ "$rc" -eq 124 ] || [ "$rc" -eq 137 ]; then
  echo "adb devices timed out after ${T}s; logcat not collected." > "$out"
elif tr -d '\r' < "$LOG_DIR/adb-devices-final.txt" | awk 'NR > 1 && $2 == "device" { found = 1 } END { exit !found }'; then
  timeout -k 2 "$T" "$ADB" logcat -d -t 4000 > "$out" 2>&1 < /dev/null
  rc=$?
  [ "$rc" -eq 0 ] || echo "[logcat exited with code $rc (124 = timed out after ${T}s); output above may be partial]" >> "$out"
else
  echo "No Android device/emulator available (adb devices rc=$rc); logcat not collected. See emulator.log for the boot failure." > "$out"
fi

timeout -k 2 "$DT" bash "$(dirname "$0")/disk-report.sh" "visual job end" > "$LOG_DIR/disk-report.txt" 2>&1 < /dev/null
rc=$?
[ "$rc" -eq 0 ] || echo "[disk report exited with code $rc (124 = timed out after ${DT}s); output above may be partial]" >> "$LOG_DIR/disk-report.txt"
exit 0
