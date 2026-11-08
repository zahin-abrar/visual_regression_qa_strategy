#!/usr/bin/env bash
# Install the APK exactly as before (adb install -r -g), with pre-install diagnostics and, on failure,
# concise post-mortem evidence. The original exit status is preserved. No retries, no --no-streaming.
# Inputs: APK_PATH, LOG_DIR. Test overrides: ADB, INSTALL_TIMEOUT.
set -u
: "${APK_PATH:?APK_PATH not set}" "${LOG_DIR:?LOG_DIR not set}"
ADB=${ADB:-adb}
IT=${INSTALL_TIMEOUT:-300}
D="$LOG_DIR/install"; mkdir -p "$D"
a() { timeout -k 2 "${1}" "$ADB" "${@:2}" 2>&1 < /dev/null; }

echo "== pre-install diagnostics =="
a 10 devices | tr -d '\r' | awk 'NR>1 && NF { print "adb state: " $0 }'
pm_n=$(a 15 shell cmd package list packages | grep -c '^package:' || true)
echo "package manager answered: ${pm_n:-0} packages"
echo "APK: $(stat -c '%s bytes' "$APK_PATH" 2>/dev/null || echo missing) sha256 $(sha256sum "$APK_PATH" 2>/dev/null | cut -d' ' -f1)"
echo "host free disk: $(df -h --output=avail,pcent / 2>/dev/null | tail -n 1 | tr -s ' ')"
echo "guest /data: $(a 10 shell df -h /data | tail -n 1 | tr -s ' ')"
echo "guest MemAvailable: $(a 10 shell grep MemAvailable /proc/meminfo | tr -s ' ')"

timeout -k 5 "$IT" "$ADB" install -r -g "$APK_PATH" > "$D/install.log" 2>&1 < /dev/null
rc=$?
cat "$D/install.log"
if [ "$rc" -eq 0 ]; then echo "install exit status: 0"; exit 0; fi

echo "::error title=APK install failed::adb install exited with status $rc (124 = timed out after ${IT}s)"
{
  echo "install exit status: $rc"
  echo "== adb state after failure =="; a 10 devices
  echo "== surfaceflinger pid: $(a 10 shell pidof surfaceflinger | tr -d '\r\n') ; system_server pid: $(a 10 shell pidof system_server | tr -d '\r\n')"
  echo "== package manager responsive: $(a 15 shell cmd package list packages | grep -c '^package:') packages"
  echo "== logcat (filtered, last 80 lines) =="
  a 20 logcat -d -t 3000 -v time | grep -E "surfaceflinger|system_server|Fatal signal|FATAL|PackageManager|lowmemorykiller|am_kill|hasReadColorBufferDma" | tail -n 80
} > "$D/install-failure.txt" 2>&1
head -n 40 "$D/install-failure.txt" | cut -c1-200
exit "$rc"
