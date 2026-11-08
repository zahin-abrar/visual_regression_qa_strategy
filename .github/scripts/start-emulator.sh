#!/usr/bin/env bash
# Create and boot ONE headless AVD "Pixel_10" mirroring the golden profile pixel10-api37
# (API 37 Google Play 16 KB x86_64 image, 1080x2424 @ 420 dpi). Bounded waits only.
set -eu
: "${ANDROID_HOME:?ANDROID_HOME not set}" "${LOG_DIR:?LOG_DIR not set}"
IMAGE="system-images;android-37.0;google_apis_playstore_ps16k;x86_64"
SDKM="$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager"
AVDM="$ANDROID_HOME/cmdline-tools/latest/bin/avdmanager"
export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH"
mkdir -p "$LOG_DIR"

echo "::group::Install emulator package and system image"
yes | "$SDKM" --licenses >/dev/null 2>&1 || true
"$SDKM" --install "platform-tools" "emulator" "$IMAGE" 2>&1 | tail -n 25
echo "::endgroup::"
emulator -version 2>&1 | head -n 3 || true

echo "::group::Create AVD"
# The pixel_10 hardware profile may be missing from older cmdline-tools; the display is forced below anyway.
if ! echo no | "$AVDM" create avd -n Pixel_10 -k "$IMAGE" --device pixel_10 --force 2>&1; then
  echo "pixel_10 device definition unavailable; falling back to pixel_9 and overriding display"
  echo no | "$AVDM" create avd -n Pixel_10 -k "$IMAGE" --device pixel_9 --force
fi
CFG="$HOME/.android/avd/Pixel_10.avd/config.ini"
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
  -accel on -gpu swiftshader_indirect > "$LOG_DIR/emulator.log" 2>&1 &
echo "emulator pid $!"

adb start-server
deadline=$(( $(date +%s) + 420 ))
until [ "$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')" = "1" ]; do
  if [ "$(date +%s)" -ge "$deadline" ]; then
    echo "::error title=Emulator boot timeout::sys.boot_completed not 1 within 420 s; see emulator.log in the infrastructure artifact"
    tail -n 40 "$LOG_DIR/emulator.log" || true
    exit 1
  fi
  sleep 5
done
adb devices -l
size=$(adb shell wm size | tr -d '\r'); dens=$(adb shell wm density | tr -d '\r')
echo "$size"; echo "$dens"
case "$size" in *"1080x2424"*) ;; *) echo "::error title=Display mismatch::expected 1080x2424, got: $size"; exit 1;; esac
case "$dens" in *"420"*) ;; *) echo "::error title=Density mismatch::expected 420 dpi, got: $dens"; exit 1;; esac
adb get-serialno
