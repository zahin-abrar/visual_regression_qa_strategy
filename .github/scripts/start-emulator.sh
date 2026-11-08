#!/usr/bin/env bash
# Create and boot ONE headless AVD "Pixel_10" mirroring the golden profile pixel10-api37
# (API 37 Google Play 16 KB x86_64 image, 1080x2424 @ 420 dpi). Bounded waits; every error propagates.
set -euo pipefail
: "${ANDROID_HOME:?ANDROID_HOME not set}" "${LOG_DIR:?LOG_DIR not set}"
IMAGE="system-images;android-37.0;google_apis_playstore_ps16k;x86_64"
IMAGE_DIR="$ANDROID_HOME/system-images/android-37.0/google_apis_playstore_ps16k/x86_64"
SDKM="$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager"
AVDM="$ANDROID_HOME/cmdline-tools/latest/bin/avdmanager"
export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH"
mkdir -p "$LOG_DIR"
fail() { echo "::error title=$1::$2"; exit 1; }

[ -x "$SDKM" ] && [ -x "$AVDM" ] || fail "cmdline-tools missing" "sdkmanager/avdmanager not found under $ANDROID_HOME/cmdline-tools/latest"

# ---- Command-line Tools diagnostics: the binaries actually invoked below, not just whatever is on PATH ----
echo "::group::Command-line Tools diagnostics"
echo "ANDROID_HOME=$ANDROID_HOME"
echo "JAVA_HOME=${JAVA_HOME:-unset}"; java -version 2>&1 | head -n 1 || true
echo "PATH sdkmanager: $(command -v sdkmanager || echo none); PATH avdmanager: $(command -v avdmanager || echo none)"
echo "invoked sdkmanager: $SDKM"; echo "invoked avdmanager: $AVDM"
echo "cmdline-tools directories: $(ls "$ANDROID_HOME/cmdline-tools" 2>/dev/null | tr '\n' ' ')"
cli_version() { timeout 60 "$1" --version 2>&1 < /dev/null | tr -d '\r' | grep -E '^[0-9]' | head -n 1 || true; }
echo "invoked sdkmanager --version: $(cli_version "$SDKM")"
timeout 90 "$SDKM" --list_installed 2>&1 < /dev/null | grep -E 'cmdline-tools|system-images|emulator|platform-tools' | head -n 12 || true
echo "selected system image: $IMAGE"
echo "::endgroup::"

echo "::group::Install emulator package and system image"
yes | "$SDKM" --licenses > "$LOG_DIR/sdkmanager-licenses.log" 2>&1 || true
timeout 900 "$SDKM" --install "platform-tools" "emulator" "$IMAGE" > "$LOG_DIR/sdkmanager-install.log" 2>&1 \
  || { tail -n 30 "$LOG_DIR/sdkmanager-install.log"; fail "sdkmanager install failed" "could not install emulator or $IMAGE"; }
tail -n 10 "$LOG_DIR/sdkmanager-install.log"
echo "::endgroup::"
[ -f "$IMAGE_DIR/system.img" ] || fail "System image missing" "$IMAGE_DIR/system.img not found after install; API level is not switched silently"

# The emulator binary must load (this is where a missing libpulse.so.0 shows up).
emulator -version > "$LOG_DIR/emulator-version.txt" 2>&1 \
  || { cat "$LOG_DIR/emulator-version.txt"; fail "emulator cannot run" "see output above (missing shared library?)"; }
head -n 3 "$LOG_DIR/emulator-version.txt"
# Optional diagnostic only. The emulator launcher sets the library search path for its bundled
# qemu engine, so a bare ldd reports bundled libraries as "not found" on a healthy install.
# This is an observation, never a failure; real library problems surface when the emulator starts.
qemu=$(ls "$ANDROID_HOME"/emulator/qemu/linux-x86_64/qemu-system-x86_64* 2>/dev/null | head -n 1 || true)
if [ -n "$qemu" ]; then
  ldd_path="$ANDROID_HOME/emulator/lib64:$ANDROID_HOME/emulator/lib64/qt/lib:$ANDROID_HOME/emulator/lib64/gles_swiftshader"
  { echo "# bare ldd (no launcher environment)"; ldd "$qemu" 2>&1 || true
    echo "# ldd with approximate launcher LD_LIBRARY_PATH"; LD_LIBRARY_PATH="$ldd_path" ldd "$qemu" 2>&1 || true; }     > "$LOG_DIR/emulator-ldd.txt"
  echo "ldd observation (informational, not a verdict): $(grep -c 'not found' "$LOG_DIR/emulator-ldd.txt" || true) 'not found' lines, see emulator-ldd.txt"
fi

echo "::group::Create AVD"
# avdmanager and the emulator launcher resolve the default AVD directory differently on the hosted
# runner (observed: AVD created under ~/.config/.android/avd, emulator looked in ~/.android/avd).
# Pin ONE directory for every tool and for the emulator process itself.
AVD_HOME="${AVD_HOME_OVERRIDE:-${RUNNER_TEMP:-/tmp}/android-avd}"
mkdir -p "$AVD_HOME"
export ANDROID_AVD_HOME="$AVD_HOME"
echo "ANDROID_AVD_HOME=$ANDROID_AVD_HOME (HOME=$HOME ANDROID_USER_HOME=${ANDROID_USER_HOME:-unset} XDG_CONFIG_HOME=${XDG_CONFIG_HOME:-unset})"
# Device definitions differ between cmdline-tools releases; pixel_9/pixel_10 are not guaranteed.
# Log what exists, then create the AVD WITHOUT --device: the golden display is forced explicitly below.
"$AVDM" list device -c > "$LOG_DIR/avdmanager-devices.txt" 2>&1 || true
echo "available device definitions: $(wc -l < "$LOG_DIR/avdmanager-devices.txt")"
# Answer avdmanager's "custom hardware profile? [no]" prompt explicitly through a pipe. Only
# avdmanager's own status counts (printf may see SIGPIPE if avdmanager exits early), and a
# timeout (124) is reported as such. The whole output is kept in avdmanager-create.log.
create_avd() {
  set +e
  printf 'no\n' | timeout -k 5 "${AVD_CREATE_TIMEOUT:-300}" "$AVDM" create avd -n Pixel_10 -k "$IMAGE" --force > "$LOG_DIR/avdmanager-create.log" 2>&1
  create_rc=${PIPESTATUS[1]}
  set -e
  echo "avdmanager create exit status: $create_rc"
  if [ "$create_rc" -ne 0 ]; then
    cat "$LOG_DIR/avdmanager-create.log"
    [ "$create_rc" -eq 124 ] && fail "AVD creation timed out" "avdmanager create avd did not finish within ${AVD_CREATE_TIMEOUT:-300} s"
    fail "AVD creation failed" "avdmanager create avd exited with status $create_rc (output above)"
  fi
  "$AVDM" list avd > "$LOG_DIR/avdmanager-list.txt" 2>&1 || true
}
CFG_DIR="$AVD_HOME/Pixel_10.avd"
CFG="$CFG_DIR/config.ini"
INI="$AVD_HOME/Pixel_10.ini"
echo "AVD home: $AVD_HOME"; echo "registration file: $INI"; echo "AVD config: $CFG"
dump() { echo "--- avdmanager create output ---"; cat "$LOG_DIR/avdmanager-create.log"
         echo "--- avdmanager list avd ---"; cat "$LOG_DIR/avdmanager-list.txt"
         echo "--- contents of $AVD_HOME ---"; ls -la "$AVD_HOME" 2>&1 || true; }
verify_registered() {
[ -f "$CFG" ] || { dump; fail "AVD not created" "avdmanager exited 0 but $CFG does not exist (output above)"; }
[ -f "$INI" ] || { dump; fail "AVD not registered" "$INI does not exist; the emulator discovers AVDs through this file"; }
reg_path=$(sed -n 's/^path=//p' "$INI" | tr -d '\r' | head -n 1)
[ "$reg_path" = "$CFG_DIR" ] || { dump; fail "AVD registration mismatch" "$INI points to '$reg_path', expected '$CFG_DIR'"; }
grep -q 'Name: Pixel_10' "$LOG_DIR/avdmanager-list.txt" || { dump; fail "AVD not listed" "avdmanager list avd (ANDROID_AVD_HOME=$ANDROID_AVD_HOME) does not show Pixel_10"; }
timeout 30 emulator -list-avds > "$LOG_DIR/emulator-list-avds.txt" 2>&1 < /dev/null || true
grep -qx 'Pixel_10' "$LOG_DIR/emulator-list-avds.txt" \
  || { dump; echo "--- emulator -list-avds ---"; cat "$LOG_DIR/emulator-list-avds.txt"; fail "AVD not visible to emulator" "emulator -list-avds (ANDROID_AVD_HOME=$ANDROID_AVD_HOME) does not list Pixel_10"; }
echo "emulator -list-avds: $(tr '\n' ' ' < "$LOG_DIR/emulator-list-avds.txt")"
}

# API 37 metadata check. Older Command-line Tools are reported (runner-images issue 14484) to write
# target=android-0 for android-37.0 images; such an AVD later crashes surfaceflinger. Never patched by hand.
EXPECTED_TARGET="android-37.0"
EXPECTED_SYSDIR="system-images/android-37.0/google_apis_playstore_ps16k/x86_64"
META_ERR=""
check_target() {
  META_ERR=""
  local t sd
  t=$(sed -n 's/^target=//p' "$INI" | tr -d '\r' | head -n 1)
  sd=$(sed -n 's/^image\.sysdir\.1=//p' "$CFG" | tr -d '\r' | head -n 1)
  sd=${sd//\\//}; sd=${sd%/}
  echo "AVD metadata: $INI target='${t:-<absent>}'; $CFG image.sysdir.1='${sd:-<absent>}'"
  if [ -z "$t" ]; then META_ERR="target= is absent from $INI"
  elif [ "$t" = "android-0" ]; then META_ERR="target=android-0 in $INI (expected $EXPECTED_TARGET); typical of Command-line Tools that do not understand dotted API 37.0 targets"
  elif [ "$t" != "$EXPECTED_TARGET" ]; then META_ERR="target='$t' in $INI, expected '$EXPECTED_TARGET' (another API level)"
  elif [ -z "$sd" ]; then META_ERR="image.sysdir.1 is absent from $CFG"
  elif [ "$sd" != "$EXPECTED_SYSDIR" ]; then META_ERR="image.sysdir.1='$sd' in $CFG, expected '$EXPECTED_SYSDIR'"
  fi
  [ -z "$META_ERR" ]
}

# Select Command-line Tools 22.0 (understands android-37.0). Versioned location, explicit binaries;
# any cmdline-tools/* directory whose sdkmanager reports 22.0 is accepted (covers a latest-2 layout).
CLI_WANTED="22.0"
find_cli_wanted() {
  local d v
  for d in "$ANDROID_HOME"/cmdline-tools/*/; do
    [ -x "${d}bin/sdkmanager" ] && [ -x "${d}bin/avdmanager" ] || continue
    v=$(cli_version "${d}bin/sdkmanager")
    case "$v" in "$CLI_WANTED"*) echo "${d%/}"; return 0;; esac
  done
  return 1
}
select_cli_wanted() {
  local dir
  if ! dir=$(find_cli_wanted); then
    echo "installing cmdline-tools;$CLI_WANTED (current invoked version: $(cli_version "$SDKM"))"
    timeout 600 "$SDKM" --install "cmdline-tools;$CLI_WANTED" > "$LOG_DIR/sdkmanager-cli-install.log" 2>&1 < /dev/null \
      || { tail -n 20 "$LOG_DIR/sdkmanager-cli-install.log"; fail "Command-line Tools install failed" "could not install cmdline-tools;$CLI_WANTED (see sdkmanager-cli-install.log)"; }
    dir=$(find_cli_wanted) || fail "Command-line Tools $CLI_WANTED not found" "installed cmdline-tools;$CLI_WANTED but no cmdline-tools/*/bin/sdkmanager reports $CLI_WANTED; found: $(ls "$ANDROID_HOME/cmdline-tools" | tr '\n' ' ')"
  fi
  SDKM="$dir/bin/sdkmanager"; AVDM="$dir/bin/avdmanager"
  echo "using Command-line Tools $CLI_WANTED: $AVDM (version $(cli_version "$SDKM"))"
}

create_avd
verify_registered
if ! check_target; then
  echo "::warning title=AVD metadata::$META_ERR"
  case "$(cli_version "$SDKM")" in "$CLI_WANTED"*) fail "AVD target metadata wrong" "$META_ERR; Command-line Tools $CLI_WANTED already in use, so this is not the old-CLI problem";; esac
  echo "Command-line Tools $(cli_version "$SDKM") produced incorrect metadata; switching to $CLI_WANTED and recreating the AVD"
  select_cli_wanted
  create_avd
  verify_registered
  check_target || fail "AVD target metadata wrong" "$META_ERR (even with Command-line Tools $CLI_WANTED)"
fi
echo "AVD metadata verified: target=$EXPECTED_TARGET, image matches $IMAGE"
python3 - "$CFG" <<'PY'
import sys
p = sys.argv[1]
want = {"hw.lcd.width": "1080", "hw.lcd.height": "2424", "hw.lcd.density": "420",
        "hw.ramSize": "4096", "disk.dataPartition.size": "6G", "hw.keyboard": "yes",
        "skin.dynamic": "yes", "fastboot.forceColdBoot": "yes"}
lines = [l for l in open(p).read().splitlines()
         if l.split("=")[0].strip() not in want and not l.startswith("skin.path")]
lines += [f"{k}={v}" for k, v in want.items()]
open(p, "w").write("\n".join(lines) + "\n")
PY
grep -E "^(hw\.lcd|hw\.ramSize|image\.sysdir|hw\.device\.name|skin\.)" "$CFG" || true
echo "::endgroup::"

# ---- ADB authentication: key pair first, then a fresh adb server, then the emulator ----
here=$(cd "$(dirname "$0")" && pwd)
for v in ANDROID_USER_HOME ANDROID_SDK_HOME; do
  if [ -n "${!v:-}" ]; then echo "note: unsetting $v (was set) so adb and the emulator both use \$HOME/.android"; unset "$v"; fi
done
bash "$here/init-adb-auth.sh" || exit 1
# A server started earlier (e.g. by sdkmanager/platform-tools) may have missed the key: restart once.
timeout 15 adb kill-server > "$LOG_DIR/adb-kill.log" 2>&1 < /dev/null || true
timeout 30 adb start-server > "$LOG_DIR/adb-start.log" 2>&1 < /dev/null || true  # redirected: daemon must not inherit this pipe

nohup emulator -avd Pixel_10 -no-window -no-audio -no-boot-anim -no-snapshot -no-metrics \
  -accel on -gpu swiftshader_indirect > "$LOG_DIR/emulator.log" 2>&1 < /dev/null &
emu=$!
echo "emulator pid $emu"

# adb transport state of the emulator: absent | offline | unauthorized | device | other
adb_state() {
  timeout 10 adb devices > "$LOG_DIR/adb-devices-poll.txt" 2>&1 < /dev/null || true
  local s
  s=$(tr -d '\r' < "$LOG_DIR/adb-devices-poll.txt" | awk '$1 ~ /^emulator-/ { print $2; exit }')
  echo "${s:-absent}"
}
start=$(date +%s); BOOT_TIMEOUT=${BOOT_TIMEOUT:-420}; deadline=$(( start + BOOT_TIMEOUT )); last=""; boot=""
while :; do
  if ! kill -0 "$emu" 2>/dev/null; then
    status=0; wait "$emu" || status=$?
    echo "--- emulator.log (last 60 lines) ---"; tail -n 60 "$LOG_DIR/emulator.log" || true
    if grep -qE 'error while loading shared libraries|cannot open shared object' "$LOG_DIR/emulator.log"; then
      echo "::error title=Emulator library missing::a shared library could not be loaded (see emulator.log above)"
    fi
    fail "Emulator process failed" "emulator process died before boot completed (exit status $status); see emulator.log above"
  fi
  state=$(adb_state)
  if [ "$state" != "$last" ]; then echo "[$(( $(date +%s) - start ))s] adb state: $state"; last=$state; fi
  if [ "$state" = "device" ]; then
    # Only an authorized transport can answer this.
    boot=$(timeout 10 adb shell getprop sys.boot_completed 2>/dev/null < /dev/null | tr -d '\r' || true)
    [ "$boot" = "1" ] && break
  fi
  if [ "$(date +%s)" -ge "$deadline" ]; then
    tail -n 40 "$LOG_DIR/emulator.log" || true
    case "$state" in
      absent)       fail "Emulator alive but no ADB transport" "no emulator-* device in adb devices after ${BOOT_TIMEOUT} s (emulator pid still running)";;
      offline)      fail "ADB transport offline" "device stayed offline for ${BOOT_TIMEOUT} s";;
      unauthorized) fail "ADB unauthorized" "device stayed unauthorized for ${BOOT_TIMEOUT} s; check adb key pair (init-adb-auth output) and emulator.log adbkey warnings";;
      device)       fail "ADB connected but Android not boot-complete" "sys.boot_completed='${boot:-}' after ${BOOT_TIMEOUT} s";;
      *)            fail "ADB unexpected state" "adb state '$state' after ${BOOT_TIMEOUT} s";;
    esac
  fi
  sleep "${POLL_INTERVAL:-5}"
done
echo "[$(( $(date +%s) - start ))s] sys.boot_completed=1"
timeout 10 adb devices -l < /dev/null
size=$(timeout 10 adb shell wm size < /dev/null | tr -d '\r'); dens=$(timeout 10 adb shell wm density < /dev/null | tr -d '\r')
echo "$size"; echo "$dens"
case "$size" in *"1080x2424"*) ;; *) fail "Display mismatch" "expected 1080x2424, got: $size";; esac
case "$dens" in *"420"*) ;; *) fail "Density mismatch" "expected 420 dpi, got: $dens";; esac
timeout 10 adb get-serialno < /dev/null

# Post-boot stabilization gate: boot_completed alone is not proof of a healthy system (surfaceflinger
# and system_server crashed seconds after boot in a real run). Bounded observation window.
EMU_PID="$emu" bash "$here/post-boot-health.sh" || exit 1
