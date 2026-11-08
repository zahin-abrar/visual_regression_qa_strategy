#!/usr/bin/env bash
# Create (or reuse) the runner-local ADB key pair BEFORE the emulator starts. The emulator copies
# $KEY_DIR/adbkey.pub into the guest to authorize this host; without a key the device stays
# "unauthorized". Keys are generated on this ephemeral runner only, never printed, never uploaded.
# Overrides for tests: ADB (adb binary), ADB_KEY_DIR (default $HOME/.android).
set -euo pipefail
ADB=${ADB:-adb}
KEY_DIR=${ADB_KEY_DIR:-$HOME/.android}
KEY="$KEY_DIR/adbkey"
PUB="$KEY.pub"
fail() { echo "::error title=$1::$2"; exit 1; }

echo "user: $(id -un) (uid $(id -u)); HOME=$HOME; key dir: $KEY_DIR"
"$ADB" version 2>&1 | head -n 2 || true

# Key-directory overrides would make adb and the emulator disagree about where the key lives.
for v in ANDROID_USER_HOME ANDROID_SDK_HOME; do
  val=${!v:-}
  if [ -n "$val" ] && [ "$val" != "$KEY_DIR" ]; then
    fail "ADB key location mismatch" "$v=$val would redirect adb away from $KEY_DIR (the emulator uses \$HOME/.android); unset it before starting adb"
  fi
done
for v in ADB_VENDOR_KEYS ANDROID_VENDOR_KEYS; do
  [ -z "${!v:-}" ] || echo "note: $v is set (not modified)"
done

"$ADB" help 2>&1 | grep -q 'keygen' || fail "adb keygen unsupported" "installed adb has no 'keygen' command; platform-tools too old"

mkdir -p "$KEY_DIR" || fail "ADB key dir" "cannot create $KEY_DIR"
chmod 700 "$KEY_DIR" || fail "ADB key dir" "cannot set permissions on $KEY_DIR"
[ -d "$KEY_DIR" ] && [ -r "$KEY_DIR" ] && [ -w "$KEY_DIR" ] && [ -x "$KEY_DIR" ] \
  || fail "ADB key dir" "$KEY_DIR is not readable/writable/searchable by $(id -un)"

if [ -s "$KEY" ] && [ -s "$PUB" ] && [ -r "$KEY" ]; then
  echo "existing non-empty key pair found; not regenerating"
else
  rm -f "$KEY" "$PUB"
  set +e
  timeout -k 2 30 "$ADB" keygen "$KEY" > /dev/null 2>"$KEY_DIR/.keygen.err" < /dev/null
  rc=$?
  set -e
  if [ "$rc" -ne 0 ]; then
    echo "adb keygen exit status $rc; stderr (key material is never written there):"; head -c 400 "$KEY_DIR/.keygen.err" || true
    rm -f "$KEY_DIR/.keygen.err"
    fail "ADB key generation failed" "adb keygen exited with status $rc (124 = timed out)"
  fi
  rm -f "$KEY_DIR/.keygen.err"
fi

[ -s "$KEY" ] || fail "ADB key missing" "$KEY does not exist or is empty after keygen"
[ -s "$PUB" ] || fail "ADB public key missing" "$PUB does not exist or is empty after keygen"
chmod 600 "$KEY"; chmod 644 "$PUB"
[ -r "$KEY" ] || fail "ADB key unreadable" "$KEY is not readable by $(id -un)"
for f in "$KEY" "$PUB"; do
  echo "$(basename "$f"): $(stat -c 'type=%F owner=%U mode=%a size=%s bytes' "$f")"
done
echo "ADB key pair ready"
