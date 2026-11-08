#!/usr/bin/env bash
# Record the environment that produced (or failed to produce) screenshots. Best-effort, no secrets.
set -u
out="${LOG_DIR:?}/environment.txt"
{
  echo "date_utc=$(date -u +%FT%TZ)"
  echo "runner_image=${ImageOS:-?} ${ImageVersion:-?}"; uname -srm
  echo "golden_profile=${VVP_GOLDEN_PROFILE:-pixel10-api37}"
  python --version 2>&1; node --version; java -version 2>&1 | head -n 1
  echo "appium=$(appium --version 2>&1)"; appium driver list --installed 2>&1
  emulator -version 2>&1 | head -n 2
  adb devices -l
  for p in ro.build.fingerprint ro.build.version.release ro.build.version.sdk ro.product.cpu.abi persist.sys.locale ro.product.locale ro.kernel.qemu.gles ro.hardware.egl; do
    echo "$p=$(adb shell getprop $p | tr -d '\r')"
  done
  adb shell wm size; adb shell wm density
  for s in "system font_scale" "global window_animation_scale" "global transition_animation_scale" "global animator_duration_scale"; do
    echo "$s=$(adb shell settings get $s | tr -d '\r')"
  done
  adb shell cmd uimode night 2>&1
  adb shell dumpsys package de.volksverpetzer.app | grep -E "versionName|versionCode|lastUpdateTime" | head -n 4
  if [ -f "${APK_PATH:-/nonexistent}" ]; then sha256sum "$APK_PATH"; fi
} > "$out" 2>&1
echo "wrote $out"
