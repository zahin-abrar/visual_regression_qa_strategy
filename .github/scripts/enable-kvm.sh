#!/usr/bin/env bash
# Apply the minimal udev rule that makes /dev/kvm usable by the runner user, wait (bounded) for
# udev to finish, print diagnostics, then decide by a FUNCTIONAL check (kvm_check.py): open
# /dev/kvm O_RDWR and issue KVM_GET_API_VERSION. Shell -r/-w tests are diagnostics only.
# Hardware acceleration stays mandatory: no software-emulation or runner fallback.
# Overrides for tests: KVM_DEVICE, SKIP_UDEV=1, PYTHON.
set -u
DEV=${KVM_DEVICE:-/dev/kvm}
PY=${PYTHON:-python3}
here=$(cd "$(dirname "$0")" && pwd)

echo "::group::KVM diagnostics (before udev)"
echo "image: ${ImageOS:-?} ${ImageVersion:-?}; runner: ${RUNNER_OS:-?}/${RUNNER_ARCH:-?}"
uname -srm
echo "user: $(id)"
grep -cE 'vmx|svm' /proc/cpuinfo 2>/dev/null | sed 's/^/cpu virtualization flag lines: /' || true
ls -l "$DEV" 2>&1 || true
stat "$DEV" 2>&1 || true
echo "::endgroup::"

if [ "${SKIP_UDEV:-0}" != "1" ]; then
  echo "::group::Apply KVM udev rule and wait for udev"
  echo 'KERNEL=="kvm", GROUP="kvm", MODE="0666", OPTIONS+="static_node=kvm"' | sudo tee /etc/udev/rules.d/99-kvm4all.rules >/dev/null \
    || { echo "::error title=KVM udev rule not written::could not write /etc/udev/rules.d/99-kvm4all.rules"; exit 1; }
  sudo udevadm control --reload-rules || echo "::warning title=udev reload failed::udevadm control --reload-rules exited $?"
  sudo udevadm trigger --name-match=kvm || echo "::warning title=udev trigger failed::udevadm trigger exited $?"
  # Bounded wait for the queued udev events (applies the rule) instead of checking immediately.
  if sudo timeout 15 udevadm settle --timeout=10; then
    echo "udev settle: completed"
  else
    echo "::warning title=udev settle::udevadm settle did not complete within its bound (exit $?); continuing to the functional check"
  fi
  echo "::endgroup::"
fi

echo "::group::KVM diagnostics (after udev)"
ls -l "$DEV" 2>&1 || true
stat "$DEV" 2>&1 || true
if [ -e "$DEV" ]; then echo "exists: yes"; else echo "exists: no"; fi
if [ -c "$DEV" ]; then echo "character device: yes"; else echo "character device: no"; fi
if [ -r "$DEV" ]; then echo "shell readable (-r): yes"; else echo "shell readable (-r): no"; fi
if [ -w "$DEV" ]; then echo "shell writable (-w): yes"; else echo "shell writable (-w): no"; fi
echo "::endgroup::"

# Authoritative decision: direct open + KVM ioctl, time-limited.
KVM_DEVICE="$DEV" timeout -k 2 20 "$PY" "$here/kvm_check.py"
rc=$?
if [ "$rc" -eq 124 ] || [ "$rc" -eq 137 ]; then
  echo "::error title=KVM check timed out::kvm_check.py did not finish within 20 s"
  exit 1
fi
if [ "$rc" -ne 0 ]; then
  echo "KVM preflight failed with code $rc (10 missing, 11 not char device, 12 access denied, 13 open failed, 14 ioctl failed, 15 unexpected API version). No software-emulation fallback."
  exit 1
fi
exit 0
