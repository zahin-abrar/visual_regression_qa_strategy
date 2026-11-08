#!/usr/bin/env bash
# Make /dev/kvm usable by the runner user, or fail with a clear message. No runner switching.
set -eu
echo 'KERNEL=="kvm", GROUP="kvm", MODE="0666", OPTIONS+="static_node=kvm"' | sudo tee /etc/udev/rules.d/99-kvm4all.rules >/dev/null
sudo udevadm control --reload-rules
sudo udevadm trigger --name-match=kvm || true
if [ ! -c /dev/kvm ] || [ ! -r /dev/kvm ] || [ ! -w /dev/kvm ]; then
  ls -l /dev/kvm 2>&1 || true
  echo "::error title=KVM unavailable::/dev/kvm is missing or not accessible on this runner. A hardware-accelerated x86_64 emulator is not possible here; not falling back to software emulation or another runner."
  exit 1
fi
ls -l /dev/kvm
