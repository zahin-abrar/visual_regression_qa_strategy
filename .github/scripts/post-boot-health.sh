#!/usr/bin/env bash
# Bounded post-boot health gate. For HEALTH_SECONDS (default 45) it requires, at every poll:
#   emulator process alive; adb state "device"; surfaceflinger and system_server present with the
#   SAME pid as at the first poll; the package manager answering a read-only query; and no fatal
#   graphics-crash signature in logcat since the gate started. Never clears logcat.
# Inputs: EMU_PID (required), LOG_DIR (required). Test overrides: ADB, HEALTH_SECONDS, HEALTH_INTERVAL,
# QUERY_TIMEOUT. Exit 0 healthy, 1 with a distinct ::error:: reason otherwise.
set -u
: "${EMU_PID:?EMU_PID not set}" "${LOG_DIR:?LOG_DIR not set}"
ADB=${ADB:-adb}
DURATION=${HEALTH_SECONDS:-45}
INTERVAL=${HEALTH_INTERVAL:-5}
QT=${QUERY_TIMEOUT:-10}
H="$LOG_DIR/health"; mkdir -p "$H"
SIGNATURES='hasReadColorBufferDma|Fatal signal [0-9]+ .*surfaceflinger|surfaceflinger.*(Fatal signal|has died|binderDied)|>>> .*surfaceflinger <<<'

q() { # q <outfile> <adb args...>; sets Q_RC; bounded; output to a file, never inherited pipes
  local out=$1; shift
  timeout -k 2 "$QT" "$ADB" "$@" > "$out" 2>&1 < /dev/null; Q_RC=$?
}
adb_state() {
  q "$H/devices.txt" devices
  local s; s=$(tr -d '\r' < "$H/devices.txt" | awk '$1 ~ /^emulator-/ { print $2; exit }')
  echo "${s:-absent}"
}
evidence() {
  { echo "== adb devices =="; cat "$H/devices.txt" 2>/dev/null
    echo "== pids: surfaceflinger=${sf0:-?}->${sf:-?} system_server=${ss0:-?}->${ss:-?} =="
    echo "== logcat (filtered, last 120 lines) =="
    timeout -k 2 20 "$ADB" logcat -d -t 3000 -v time 2>&1 < /dev/null \
      | grep -E "surfaceflinger|system_server|Fatal signal|FATAL|lowmemorykiller|am_kill|ANR in|hasReadColorBufferDma" | tail -n 120
  } > "$H/health-failure.txt" 2>&1
  echo "evidence written to $H/health-failure.txt"
}
bad() { # bad <title> <message>
  echo "::error title=Emulator unhealthy: $1::$2"
  evidence
  exit 1
}
pid_of() { # pid_of <process>; prints pid, "MISSING", or "UNKNOWN" (transient adb failure)
  q "$H/pid.txt" shell pidof "$1"
  local p; p=$(tr -d '\r\n ' < "$H/pid.txt")
  if [ "$Q_RC" -eq 124 ] || grep -qE 'error:|closed|offline|unauthorized' "$H/pid.txt"; then echo UNKNOWN
  elif [ -z "$p" ]; then echo MISSING
  else echo "$p"; fi
}

start=$(date +%s); hard=$(( start + DURATION + 120 ))
dev_since=$(timeout -k 2 "$QT" "$ADB" shell date '+%m-%d %H:%M:%S.000' 2>/dev/null < /dev/null | tr -d '\r')
sf0=""; ss0=""; sf=""; ss=""; unknown=0; polls=0
echo "health gate: ${DURATION}s window, ${INTERVAL}s interval, device time at start: ${dev_since:-unknown}"
while :; do
  polls=$(( polls + 1 ))
  [ "$(date +%s)" -le "$hard" ] || bad "gate overran" "health gate exceeded its hard limit"
  kill -0 "$EMU_PID" 2>/dev/null || bad "emulator exited" "emulator process $EMU_PID is no longer running (poll $polls)"
  st=$(adb_state)
  [ "$st" = "device" ] || bad "adb $st" "adb state is '$st', expected 'device' (poll $polls)"

  sf=$(pid_of surfaceflinger); ss=$(pid_of system_server)
  if [ "$sf" = UNKNOWN ] || [ "$ss" = UNKNOWN ]; then
    unknown=$(( unknown + 1 ))
    [ "$unknown" -lt 2 ] || bad "adb unresponsive" "pidof queries failed or timed out twice in a row (poll $polls)"
  else
    unknown=0
    [ "$sf" != MISSING ] || bad "surfaceflinger missing" "pidof surfaceflinger found nothing (poll $polls; was '${sf0:-none}')"
    [ "$ss" != MISSING ] || bad "system_server missing" "pidof system_server found nothing (poll $polls; was '${ss0:-none}')"
    [ -n "$sf0" ] || sf0=$sf
    [ -n "$ss0" ] || ss0=$ss
    [ "$sf" = "$sf0" ] || bad "surfaceflinger restarted" "pid changed $sf0 -> $sf (poll $polls)"
    [ "$ss" = "$ss0" ] || bad "system_server restarted" "pid changed $ss0 -> $ss (poll $polls)"
  fi

  q "$H/pm.txt" shell cmd package list packages
  [ "$Q_RC" -ne 124 ] || bad "package manager timeout" "cmd package list packages did not answer within ${QT}s (poll $polls)"
  { [ "$Q_RC" -eq 0 ] && grep -q '^package:' "$H/pm.txt"; } || bad "package manager not answering" "cmd package list packages exit $Q_RC, no package lines (poll $polls)"

  if [ -n "$dev_since" ]; then
    timeout -k 2 20 "$ADB" logcat -d -v time -b main,system,crash -T "$dev_since" > "$H/logcat-window.txt" 2>&1 < /dev/null
  else
    timeout -k 2 20 "$ADB" logcat -d -v time -b main,system,crash -t 500 > "$H/logcat-window.txt" 2>&1 < /dev/null
  fi
  if grep -E "$SIGNATURES" "$H/logcat-window.txt" > "$H/signature-hits.txt" 2>/dev/null && [ -s "$H/signature-hits.txt" ]; then
    echo "fatal graphics signature(s) observed:"; head -n 5 "$H/signature-hits.txt" | cut -c1-200
    bad "fatal graphics crash" "surfaceflinger assertion/fatal signal in logcat during the observation window (poll $polls)"
  fi

  [ "$(( $(date +%s) - start ))" -lt "$DURATION" ] || break
  sleep "$INTERVAL"
done
echo "health gate passed: $polls polls over $(( $(date +%s) - start ))s; surfaceflinger pid $sf0, system_server pid $ss0 stable; package manager responsive; no fatal signatures"
