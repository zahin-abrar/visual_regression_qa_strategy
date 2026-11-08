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
# Device definitions differ between cmdline-tools releases; pixel_9/pixel_10 are not guaranteed.
# Log what exists, then create the AVD WITHOUT --device: the golden display is forced explicitly below.
"$AVDM" list device -c > "$LOG_DIR/avdmanager-devices.txt" 2>&1 || true
echo "available device definitions: $(wc -l < "$LOG_DIR/avdmanager-devices.txt")"
"$AVDM" create avd -n Pixel_10 -k "$IMAGE" --force <<< "no" >"$LOG_DIR/avdmanager-create.log" 2>&1 \
  || { cat "$LOG_DIR/avdmanager-create.log"; fail "AVD creation failed" "avdmanager create avd exited nonzero"; }
CFG="$HOME/.android/avd/Pixel_10.avd/config.ini"
[ -f "$CFG" ] || { cat "$LOG_DIR/avdmanager-create.log"; fail "AVD not created" "$CFG does not exist"; }
"$AVDM" list avd > "$LOG_DIR/avdmanager-list.txt" 2>&1 || true
grep -q 'Name: Pixel_10' "$LOG_DIR/avdmanager-list.txt" || fail "AVD not listed" "avdmanager list avd does not show Pixel_10"
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

nohup emulator -avd Pixel_10 -no-window -no-audio -no-boot-anim -no-snapshot -no-metrics \
  -accel on -gpu swiftshader_indirect > "$LOG_DIR/emulator.log" 2>&1 < /dev/null &
emu=$!
echo "emulator pid $emu"

# Redirected so the adb daemon does not inherit this step's output pipe.
timeout 30 adb start-server > "$LOG_DIR/adb-start.log" 2>&1 < /dev/null || true
deadline=$(( $(date +%s) + 420 ))
until [ "$(timeout 10 adb shell getprop sys.boot_completed 2>/dev/null < /dev/null | tr -d '\r')" = "1" ]; do
  if ! kill -0 "$emu" 2>/dev/null; then
    status=0; wait "$emu" || status=$?
    echo "--- emulator.log (last 60 lines) ---"; tail -n 60 "$LOG_DIR/emulator.log" || true
    if grep -qE 'error while loading shared libraries|cannot open shared object' "$LOG_DIR/emulator.log"; then
      echo "::error title=Emulator library missing::a shared library could not be loaded (see emulator.log above)"
    fi
    fail "Emulator exited" "emulator process died before boot completed (exit status $status); see emulator.log above"
  fi
  if [ "$(date +%s)" -ge "$deadline" ]; then
    tail -n 40 "$LOG_DIR/emulator.log" || true
    fail "Emulator boot timeout" "sys.boot_completed not 1 within 420 s"
  fi
  sleep 5
done
timeout 10 adb devices -l < /dev/null
size=$(timeout 10 adb shell wm size < /dev/null | tr -d '\r'); dens=$(timeout 10 adb shell wm density < /dev/null | tr -d '\r')
echo "$size"; echo "$dens"
case "$size" in *"1080x2424"*) ;; *) fail "Display mismatch" "expected 1080x2424, got: $size";; esac
case "$dens" in *"420"*) ;; *) fail "Density mismatch" "expected 420 dpi, got: $dens";; esac
timeout 10 adb get-serialno < /dev/null
